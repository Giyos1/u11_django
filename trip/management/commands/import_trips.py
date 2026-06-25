import pandas as pd

from django.core.management.base import BaseCommand, CommandError

from trip.models import Trip


class Command(BaseCommand):
    help = "Excel fayldagi taksi ma'lumotlarini Trip jadvaliga yozadi."

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default="new_york_yaxi_1_mln.xlsx")
        parser.add_argument("--batch-size", type=int, default=1000)
        parser.add_argument("--truncate", action="store_true")

    def handle(self, *args, **options):
        path = options["path"]

        if options["truncate"]:
            Trip.objects.all().delete()

        try:
            df = pd.read_excel(path)
        except FileNotFoundError:
            raise CommandError(f"Fayl topilmadi: {path}")

        # NaN -> None (bazaga null bo'lib yozilishi uchun)
        df = df.where(pd.notnull(df), None)

        # pickup/dropoff datetime ustunlarini sanaga aylantiramiz (model DateField)
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce").dt.date
        df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"], errors="coerce").dt.date

        trips = [
            Trip(
                vendor_id=row["vendor_id"],
                pickup_date=row["pickup_datetime"],
                dropoff_date=row["dropoff_datetime"],
                passenger_count=row["passenger_count"],
                trip_distance=row["trip_distance"],
                pickup_Longitude=row["pickup_longitude"],
                pickup_Latitude=row["pickup_latitude"],
                rate_code=row["rate_code"],
                store_and_fwd_flag=row["store_and_fwd_flag"],
                dropoff_longitude=row["dropoff_longitude"],
                dropoff_latitude=row["dropoff_latitude"],
                payment_type=row["payment_type"],
                fare_amount=row["fare_amount"],
                surcharge=row["surcharge"],
                mta_max=row["mta_tax"],
                trip_amount=row["tip_amount"],
                tools_amount=row["tolls_amount"],
                total_amount=row["total_amount"],
            )
            for _, row in df.iterrows()
        ]

        Trip.objects.bulk_create(trips, batch_size=options["batch_size"])

        self.stdout.write(
            self.style.SUCCESS(f"Tugadi. Jami {len(trips)} ta Trip yozuvi yaratildi.")
        )