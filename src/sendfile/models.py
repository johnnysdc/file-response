from django.db import models

# Create your models here.

class UploadFileAnalisador(models.Model):

    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID',
        db_column='PK_ANAR'
    )
    analisador_name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        db_column='ANAR_NM_ANALISADOR'
    )
    modelo = models.BinaryField(
        max_length=4294967295,
        editable=True,
        db_column='ANAR_TX_MODELO'
    )
    scaler_data = models.BinaryField(
        max_length=4294967295,
        editable=True,
        db_column='ANAR_TX_SCALER_DATA'
    )

    class Meta:
        db_table = 'ARQUIVOS'

    def __str__(self):
        return self.analisador_name
