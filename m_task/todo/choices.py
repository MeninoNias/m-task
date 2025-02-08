from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _

class EpicStatusChoices(IntegerChoices):
    PLANEJADO = 1, _('Planejado')
    EM_ANDAMENTO = 2, _('Em Andamento')
    CONCLUIDO = 3, _('Concluído')
    BLOQUEADO = 4, _('Bloqueado')
    CANCELADO = 5, _('Cancelado')
    AGUARDANDO_APROVACAO = 6, _('Aguardando Aprovação')

    @classmethod
    def get_value_from_label(cls, label):
        OPTIONS = {
            "PL": cls.PLANEJADO.value,
            "EM": cls.EM_ANDAMENTO.value,
            "CO": cls.CONCLUIDO.value,
            "BL": cls.BLOQUEADO.value,
            "CA": cls.CANCELADO.value,
            "AA": cls.AGUARDANDO_APROVACAO.value,
        }
        return OPTIONS.get(label, None)
