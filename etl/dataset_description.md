# NYC Yellow Taxi Trip Sample Dataset

| Column Name              | Description |
|-------------------------|-------------|
| **VendorID**           | A code indicating the TPEP provider that provided the record.<br>1. Creative Mobile Technologies<br>2. VeriFone Inc. |
| **tpep_pickup_datetime**  | The date and time when the meter was engaged. |
| **tpep_dropoff_datetime** | The date and time when the meter was disengaged. |
| **Passenger_count**    | The number of passengers in the vehicle. This is a driver-entered value. |
| **Trip_distance**      | The elapsed trip distance in miles reported by the taximeter. |
| **Pickup_longitude**   | Longitude where the meter was engaged. |
| **Pickup_latitude**    | Latitude where the meter was engaged. |
| **RateCodeID**         | The final rate code in effect at the end of the trip.<br>1. Standard rate<br>2. JFK<br>3. Newark<br>4. Nassau or Westchester<br>5. Negotiated fare<br>6. Group ride |
| **Store_and_fwd_flag** | This flag indicates whether the trip record was held in vehicle memory before sending to the vendor (aka “store and forward”).<br>Y = store and forward trip<br>N = not a store and forward trip |
| **Dropoff_longitude**  | Longitude where the meter was disengaged. |
| **Dropoff_latitude**   | Latitude where the meter was disengaged. |
| **Payment_type**       | A numeric code signifying how the passenger paid for the trip.<br>1. Credit card<br>2. Cash<br>3. No charge<br>4. Dispute<br>5. Unknown<br>6. Voided trip |
| **Fare_amount**        | The time-and-distance fare calculated by the meter. |
| **Extra**              | Miscellaneous extras and surcharges, including the $0.50 and $1 rush hour and overnight charges. |
| **MTA_tax**           | $0.50 MTA tax that is automatically triggered based on the metered rate in use. |
| **Improvement_surcharge** | $0.30 improvement surcharge assessed at the flag drop. Began being levied in 2015. |
| **Tip_amount**         | Tip amount – Automatically populated for credit card tips. Cash tips are not included. |
| **Tolls_amount**       | Total amount of all tolls paid in trip. |
| **Total_amount**       | The total amount charged to passengers. Does not include cash tips. |