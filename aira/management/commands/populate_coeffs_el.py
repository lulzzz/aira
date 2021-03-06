#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from aira.models import CropType, IrrigationType


class Command(BaseCommand):
    help = """Populate CropType and IrrigationType tables
              of aira database with essential constant coefficients
              as Greek_name (English_name) """

    def handle(self, *args, **options):
        try:
            croptype_csv = os.path.join(settings.AIRA_PARAMETERS_FILE_DIR,
                                        'croptype_el.csv')
            irrt_csv = os.path.join(settings.AIRA_PARAMETERS_FILE_DIR,
                                    'irr_eff_el.csv')

            with open(irrt_csv) as f:
                reader = csv.reader(f)
                for row in reader:
                    irr_type = "{} ({})".format(row[1], row[0])
                    _, created = IrrigationType.objects.get_or_create(
                                                name=irr_type,
                                                efficiency=float(row[2]))

            with open(croptype_csv) as f:
                reader = csv.reader(f)
                reader.next()
                for row in reader:
                    crop = "{} ({})".format(row[1], row[0])
                    _, created = CropType.objects.get_or_create(
                                 name=crop,
                                 root_depth_min=float(row[2]),
                                 root_depth_max=float(row[3]),
                                 max_allow_depletion=float(row[4]),
                                 kc=float(row[5]),
                                 fek_category=int(row[6]),)
        except:
            raise CommandError(
                "Use 'makemigrations aira' to create aira tables")

        self.stdout.write('Aira database is successfully updated')
