import json
from django.core.management.base import BaseCommand
from locations.models import Region, Province, Commune
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = "Carga regiones, provincias y comunas de Chile desde un JSON local"

    def handle(self, *args, **kwargs):
        self.stdout.write("Cargando ubicaciones de Chile (local JSON)...")

        json_path = Path(settings.BASE_DIR) / "locations" / "data" / "chile.json"

        if not json_path.exists():
            self.stderr.write(f"❌ No se encontró el archivo: {json_path}")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # JSON = lista de regiones
        for r in data:
            region_obj, _ = Region.objects.get_or_create(
                code=str(r["id"]),
                defaults={"name": r["name"]},
            )

            for p in r["provinces"]:
                prov_obj, _ = Province.objects.get_or_create(
                    code=str(p["id"]),
                    defaults={"name": p["name"], "region": region_obj},
                )

                # Comunas → generamos code único automáticamente
                for idx, c_name in enumerate(p["communes"], start=1):
                    commune_code = f"{p['id']}{idx:02d}"

                    Commune.objects.get_or_create(
                        code=commune_code,
                        defaults={
                            "name": c_name,
                            "province": prov_obj
                        }
                    )

        self.stdout.write(self.style.SUCCESS("✓ Datos de Chile cargados correctamente."))