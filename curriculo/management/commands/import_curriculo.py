import json
from django.core.management.base import BaseCommand, CommandError
from curriculo.models import CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion
from grupos.models import Asignatura


class Command(BaseCommand):
    help = "Importa el currículo LOMLOE desde un archivo JSON"

    def add_arguments(self, parser):
        parser.add_argument("--asignatura", type=int, required=True)
        parser.add_argument("--archivo", type=str, required=True)
        parser.add_argument(
            "--modo",
            type=str,
            choices=["sobrescribir", "actualizar"],
            default="actualizar",
        )

    def handle(self, *args, **options):
        try:
            asignatura = Asignatura.objects.get(id=options["asignatura"])
        except Asignatura.DoesNotExist:
            raise CommandError(f"No existe la asignatura con id {options['asignatura']}")

        with open(options["archivo"], encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise CommandError("El archivo JSON debe contener una lista de competencias clave.")

        for cc_data in data:
            self._validar_cc(cc_data)

        if options["modo"] == "sobrescribir":
            CompetenciaClave.objects.filter(asignatura=asignatura).delete()

        codigos_cc = set()
        codigos_ce = set()
        codigos_crit = set()

        for cc_data in data:
            cc, _ = CompetenciaClave.objects.update_or_create(
                codigo=cc_data["codigo"],
                asignatura=asignatura,
                defaults={
                    "descripcion": cc_data["descripcion"],
                    "peso": cc_data.get("peso", 1.0),
                },
            )
            self.stdout.write(f"  CC {cc.codigo}")

            if cc.codigo in codigos_cc:
                self.stdout.write(self.style.WARNING(f"    Código duplicado: {cc.codigo}"))
            codigos_cc.add(cc.codigo)

            for ce_data in cc_data.get("competencias_especificas", []):
                ce, _ = CompetenciaEspecifica.objects.update_or_create(
                    codigo=ce_data["codigo"],
                    competencia_clave=cc,
                    defaults={
                        "descripcion": ce_data["descripcion"],
                        "peso": ce_data.get("peso", 1.0),
                    },
                )
                self.stdout.write(f"    CE {ce.codigo}")

                ce_key = f"{cc.codigo}.{ce.codigo}"
                if ce_key in codigos_ce:
                    self.stdout.write(
                        self.style.WARNING(f"      Código duplicado: {ce.codigo}")
                    )
                codigos_ce.add(ce_key)

                for crit_data in ce_data.get("criterios", []):
                    crit, _ = CriterioEvaluacion.objects.update_or_create(
                        codigo=crit_data["codigo"],
                        competencia_especifica=ce,
                        defaults={
                            "descripcion": crit_data["descripcion"],
                            "peso": crit_data.get("peso", 1.0),
                        },
                    )
                    self.stdout.write(f"      CRIT {crit.codigo}")

                    crit_key = f"{cc.codigo}.{ce.codigo}.{crit.codigo}"
                    if crit_key in codigos_crit:
                        self.stdout.write(
                            self.style.WARNING(f"        Código duplicado: {crit.codigo}")
                        )
                    codigos_crit.add(crit_key)

        self.stdout.write(
            self.style.SUCCESS(
                f"Currículo importado correctamente en '{asignatura}'"
            )
        )

    def _validar_cc(self, cc_data):
        if "codigo" not in cc_data or "descripcion" not in cc_data:
            raise CommandError(
                "Cada competencia clave debe tener 'codigo' y 'descripcion'."
            )
        for ce_data in cc_data.get("competencias_especificas", []):
            if "codigo" not in ce_data or "descripcion" not in ce_data:
                raise CommandError(
                    "Cada competencia específica debe tener 'codigo' y 'descripcion'."
                )
            for crit_data in ce_data.get("criterios", []):
                if "codigo" not in crit_data or "descripcion" not in crit_data:
                    raise CommandError(
                        "Cada criterio debe tener 'codigo' y 'descripcion'."
                    )
