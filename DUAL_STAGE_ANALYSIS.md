# Branded vs. Unbranded — Logprob Confidence

- **Generated:** 2026-06-23
- **Scored file:** `dual_stage_scored.csv`

Each product is classified branded/unbranded by the model in a single forced token (B/U) with logprobs on. The **confidence is the token probability mass on the chosen letter** — a real logprob, not a self-reported number. No quantity is involved.

## Headline

- **Accuracy** (vs. gold labels): **45.9%** (447/973)
- **Mean confidence:** 0.9022
- **Mean confidence when correct:** 0.9698
- **Mean confidence when wrong:** 0.8448
- **Separation (right − wrong):** +0.1249 — positive means the logprob confidence actually tracks correctness.

## Confidence by true class

| true class | n | mean confidence | accuracy |
|---|---|---|---|
| branded | 0 | — | — |
| unbranded | 785 | 0.8924 | 56.9% |

## Confidence bands

High ≥ 0.85 · Medium 0.70–0.85 · Low < 0.70.

| band | n | accuracy in band |
|---|---|---|
| high | 841 | 0.509 |
| medium | 30 | 0.233 |
| low | 102 | 0.118 |

**Grey zone (confidence ≤ 0.85 → route to review): 136 / 1000 rows (14%).** Everything above is auto-accept.

## Misclassifications

| title | true | predicted | confidence |
|---|---|---|---|
| Sakthi - Kulambu Chilli powder, 500gm | unbranded | branded | 1.0000 |
| Taski Suma Ultra (L2) 5L Can | unbranded | branded | 1.0000 |
| Red Malka (Lal Masoor) Rajdhani | unbranded | branded | 1.0000 |
| AASHIRVAAD - ATTA 10 KG BAG | aashirvaad | branded | 1.0000 |
| Cocoa powder (Medium Brown) Vanhouten | unbranded | branded | 1.0000 |
| MDH Chana Masala | unbranded | branded | 1.0000 |
| Mother Dairy milk | unbranded | branded | 1.0000 |
| SPRITE 250ML | pepsi | branded | 1.0000 |
| NATURESMITH PAPRIKA POWDER 60GM | unbranded | branded | 1.0000 |
| Bru Coffee 500g | unbranded | branded | 1.0000 |
| Nestle Milk Powder 1KG | unbranded | branded | 1.0000 |
| Coke 750 Ml | unbranded | branded | 1.0000 |
| #_# Mango Kulfi 300gm - Parsi Dairy Farm | unbranded | branded | 1.0000 |
| Biscoff Biscuit Lotus | unbranded | branded | 1.0000 |
| President Butter Unsalted 500gm | unbranded | branded | 1.0000 |
| Pizza Base 8 inch Whole Wheat Pan Crust (Junos) | unbranded | branded | 1.0000 |
| Twinings strawberry green tea | unbranded | branded | 1.0000 |
| Madhusudan Butter | unbranded | branded | 1.0000 |
| Soda Water Kinley 750 ml | unbranded | branded | 1.0000 |
| MAPRO BLACK CURRANT 1 LTR | unbranded | branded | 1.0000 |
| #_# Plain Milk Chocolate Bar 41% [65 g] - Entisi Chocolatier | unbranded | branded | 1.0000 |
| HAMDARD ROOHAFZA 750ML | unbranded | branded | 1.0000 |
| Goodlife Milk 1ltr pkt Nandini | unbranded | branded | 1.0000 |
| preethi xpro Duo mg-198 1300w | unbranded | branded | 1.0000 |
| Corn Flour Weikfield | unbranded | branded | 1.0000 |
| Tea Powder   Red Label 1kg pkt | unbranded | branded | 1.0000 |
| Cremica Chef Choice Mayo | unbranded | branded | 1.0000 |
| Tropicana Orange Juice 1 Ltr | unbrand | branded | 1.0000 |
| Hoegaarden Belgian Blanche | unbranded | branded | 1.0000 |
| Chicken Broth Powder Knorr | unbranded | branded | 1.0000 |
| Sprite 300 ml | unbranded | branded | 1.0000 |
| Tata Agni Dust Tea 1 kg | unbranded | branded | 1.0000 |
| Amul Cheese Spread 200 Gm | unbranded | branded | 1.0000 |
| MDH - White Pepper Powder 100 gm 30291 | outlet | branded | 1.0000 |
| 100 Pipers. 750Ml | unbrand | branded | 1.0000 |
| kikkoman Soya Sauce | unbranded | branded | 1.0000 |
| Coke Can 300 Ml | coca cola | branded | 1.0000 |
| RED LABEL TEA (1 KG) | unbranded | branded | 1.0000 |
| Nihari Masala  (Shan) | unbranded | branded | 1.0000 |
| Mapro Strawberry  Berry Crush-5 Ltr | unbranded | branded | 1.0000 |
| White Pepper MDH 100 Gms | unbranded | branded | 1.0000 |
| MILK AMUL TETRA PACK | amul | branded | 1.0000 |
| RAJDHANI - SOOJI (1KG) | unbranded | branded | 1.0000 |
| Milk Powder Nestle 1 Kg | unbranded | branded | 1.0000 |
| Coca cola 750ml | olio | branded | 1.0000 |
| Meat Masala MDH | unbranded | branded | 1.0000 |
| Fanta Can 300ml-GST@ 28% | unbranded | branded | 1.0000 |
| CARNATTION MILK  405 GM ( EVAPORATED MILK ) | unbranded | branded | 1.0000 |
| MONIN VANILLA SYRUP 1 L | monin | branded | 1.0000 |
| Harpic 500 Ml | unbrand | branded | 1.0000 |
| McCain Rosti Round/ Hash Brown 1.5kg | unbranded | branded | 1.0000 |
| CHANA MASALA MDH 100GM | unbranded | branded | 1.0000 |
| Agnessi Penne Pasta | unbranded | branded | 1.0000 |
| Coffee powder Nescafe 500 gm | unbranded | branded | 1.0000 |
| MTR Sambar | cfi | branded | 1.0000 |
| Truffle Oil Urbani 250 ml | unbranded | branded | 1.0000 |
| Ashok Besan | unbranded | branded | 1.0000 |
| Natural Mineral Water Aava 500 ml | unbranded | branded | 1.0000 |
| Colin Spray 500ml | unbranded | branded | 1.0000 |
| GREEN CURRY PASTE NAMJAI 1 KG | unbranded | branded | 1.0000 |
| AMUL CHEESE SP PLAIN | unbranded | branded | 1.0000 |
| Jacobs Creek Red 750Ml | unbrand | branded | 1.0000 |
| Nestle Water (19 Litre) | unbranded | branded | 1.0000 |
| #_# Strawberry Kulfi 300gm - Parsi Dairy Farm | unbranded | branded | 1.0000 |
| Mdh Dhaniya powder 500gm | unbranded | branded | 1.0000 |
| Tropicana Mango Juice 1Ltr | unbrand | branded | 1.0000 |
| MONIN HAZELNUT SYRUP 1LTR | unbranded | branded | 1.0000 |
| Thai Tea Mix 400g packet Chatramue | unbranded | branded | 1.0000 |
| Hoegaarden | unbranded | branded | 1.0000 |
| ANANDA PANEER 1 KG | ananda | branded | 1.0000 |
| Aavin Milk | unbranded | branded | 1.0000 |
| Sriracha Hot Chilli Sauce Flying Goose 730 gm | unbranded | branded | 1.0000 |
| Tata Salt 1kg | unbranded | branded | 1.0000 |
| Monin Peach Syrup | unbrand | branded | 1.0000 |
| Malas strawberry crush 750ml | unbranded | branded | 0.9999 |
| Perrier Water 330mL | unbranded | branded | 0.9999 |
| Cambro Polycarbonate GN Pan 1/2 200mm | unbranded | branded | 0.9999 |
| Premix Egg Free Chocolate Make: pillsbury | unbranded | branded | 0.9999 |
| Possmei Taro Powder Premix 1kg pkt | possmei | branded | 0.9999 |
| #_# Rocky Road Ice-cream Tub (100ml) - Meemees | unbranded | branded | 0.9999 |
| Taski R5 5ltr | unbranded | branded | 0.9999 |
| Red Yellow Capsicum Mixed | unbrand | unbranded | 0.9999 |
| Lobo - 5 Spice Powder 65 gm 51547 | outlet | branded | 0.9999 |
| Maggi Seasoning Sauce 680Ml | unbranded | branded | 0.9999 |
| Pickle Sachet | all brands | unbranded | 0.9999 |
| Delmonte - Eggless Mayo | delmonte | branded | 0.9999 |
| Oat Milk AltCo. 200 ml | unbranded | branded | 0.9999 |
| Cheddar White Wyke 2.5 Kg | unbranded | branded | 0.9999 |
| Malas Orange Crush 750ml | unbranded | branded | 0.9999 |
| Rice Flat Noodle 10mm   500g pkt   How How | unbranded | branded | 0.9999 |
| Shresth Gold Milk 500 Ml | shreeji dairy | branded | 0.9999 |
| Butter Paper 15*15 | unbrand | unbranded | 0.9999 |
| JK Copier A4 Paper | unbranded | branded | 0.9999 |
| SANDWICH BOX | ovenfresh | unbranded | 0.9999 |
| Amrut fusion single malt whisky 750 ml | unbranded | branded | 0.9999 |
| Monin Peach flavour | unbranded | branded | 0.9999 |
| Chicken wings Coated ( ITC ) | olio | branded | 0.9999 |
| Vat 69 | unbranded | branded | 0.9999 |
| Taski R7 - 5ltr Can | diversey | branded | 0.9999 |
| Micks Lotus Biscoff Biscuit | unbranded | branded | 0.9999 |
| Amul Fresh Cream 1 Ltr- Exempt | unbranded | branded | 0.9999 |
| Kitchen King MDH 100 Gm- GST @ 5% | unbranded | branded | 0.9999 |
| Pril Liquid | unbranded | branded | 0.9999 |
| Monin Raspberry | unbranded | branded | 0.9999 |
| Sarwar Onion Powder 450gm | unbranded | branded | 0.9999 |
| Cherry Tomato | unbrand | unbranded | 0.9999 |
| Pitambari Powder | unbranded | branded | 0.9999 |
| Rice flour Vijay 1KG-SNACC | unbranded | branded | 0.9999 |
| #_# Misti Doi 100gm - Parsi Dairy Farm | unbranded | branded | 0.9999 |
| Harpic 500 ml | unbranded | branded | 0.9999 |
| #_# Chocolate Coated Salted Pistachio Dragees Jar [120 grams] - Entisi Chocolatier | unbranded | branded | 0.9999 |
| ANGOSTURA Aromatic bitters (200ML) | unbranded | branded | 0.9999 |
| Possmei Passion Fruit Syrup 2.5Kg bottle | possmei | branded | 0.9999 |
| EASTMADE - CUMIN (JEERA) 1 KG | unbranded | branded | 0.9998 |
| Silken Tofu 300g Voila | unbranded | branded | 0.9998 |
| ROOH AFZA | unbranded | branded | 0.9998 |
| Malaysian Noodles ( Flat Noodles ) 1kg | outlet | unbranded | 0.9998 |
| Carrots/Gajar, incremental 0.5 10335 | outlet | unbranded | 0.9998 |
| Kit Kat | unbranded | branded | 0.9998 |
| Beer Non Alcoholic 330 ml - Coolberg (Ginger Flavour) | coolberg | branded | 0.9998 |
| PLASTIC CONTAINER 750ML | divya | unbranded | 0.9998 |
| 340 MM BOPP ROLL | ovenfresh | unbranded | 0.9998 |
| Griffith Hot Chilli Marinade | custom culinary | branded | 0.9998 |
| Active X Mustard Oil 500mL | unbranded | branded | 0.9998 |
| #_# Classic Vanilla Minis Sugar Free Ice cream [09 pieces] - Noto | unbranded | branded | 0.9998 |
| Almond biscotti (1pcs) | base kitchen | unbranded | 0.9998 |
| Artichoke Tin 390 Grms | unbrand | unbranded | 0.9998 |
| Orange Juice 1 Lltr | real | unbranded | 0.9998 |
| #_# Blueberry Greek Yogurt Minis Guilt Free Ice Cream [09 pieces] - Noto | unbranded | branded | 0.9998 |
| Chef's Art - Crispy Cajun Breading Mix 1 Kg H51176 | outlet | branded | 0.9998 |
| Fortune Aata | unbranded | branded | 0.9998 |
| #_# Double Cocoa Protien Bar - The Whole Truth | unbranded | branded | 0.9998 |
| Macroni Rajdhani | unbranded | branded | 0.9998 |
| Green Mustard Microgreen | unbrand | unbranded | 0.9998 |
| Newtrition - Lemon Ginger, 500 ML | outlet | branded | 0.9998 |
| Thums Up 250 ml | coke | branded | 0.9998 |
| Taski D9 (5lt) | unbranded | branded | 0.9998 |
| PLASTIC CONTAINER 25ML | ice packing | unbranded | 0.9998 |
| AJINO MOTO | unbranded | branded | 0.9998 |
| Aluminium (Silver) Pouches 6 inch * 9 inch (Pack of 100) 137302 | outlet | unbranded | 0.9998 |
| #_# Prasuma FS Tandoori Veg Momos - Prasuma | unbranded | branded | 0.9998 |
| Budweiser 330Ml | unbrand | branded | 0.9998 |
| #_# Cookies and Cream Ice-cream Tub (100ml) - Meemees | unbranded | branded | 0.9998 |
| Maggi Cubes Chicken | unbranded | branded | 0.9998 |
| Habit Olives Green Pitted 3Kg | unbranded | branded | 0.9998 |
| ITC Long Note Book 160 pages hard | unbranded | branded | 0.9998 |
| RICE DOSA | nandi-sln-a1 | unbranded | 0.9998 |
| White sesame Seeds 100G - Sancc | unbranded | branded | 0.9998 |
| SUMA TAB CHLORINE | unbranded | branded | 0.9997 |
| VIKRAM - CHAKKI ATTA 30 KG | unbranded | branded | 0.9997 |
| Pesto Pistachio 2.5kg (Mec3-14755) | unbranded | branded | 0.9997 |
| Coriander Fresh W/O Roots | all brands | unbranded | 0.9997 |
| DRY COCONUT | jay maruthi gold | unbranded | 0.9997 |
| #_# The Berry Good Bar 72% [Chocolate Bar] - La Folie | unbranded | branded | 0.9997 |
| Chefs Art - Jamaican Jerk Seasoning 400 gm | outlet | branded | 0.9997 |
| CHOCOLATE GANACHE (500GM) | base kitchen | unbranded | 0.9997 |
| #_# Lotus Biscoff Icecream (125ML) - Bina | unbranded | branded | 0.9997 |
| Shot Glass 60Ml | krispy kreme | unbranded | 0.9997 |
| Dabur Honey | unbranded | branded | 0.9997 |
| #_# The Great Indian Toffee 300gm - Parsi Dairy Farm | unbranded | branded | 0.9997 |
| Fevicol 1 Kg | unbranded | branded | 0.9997 |
| Rai (Mustard Seed) 100gm | zomato hyperpure | unbranded | 0.9997 |
| #_# Motichur Laddu 500gms - Dadus | unbranded | branded | 0.9997 |
| RTE-Seths - Chinese Ready Schezwan Sauce (Frozen) 1 Kg | outlet | branded | 0.9997 |
| Onion Sambar | unbrand | unbranded | 0.9997 |
| Corona Lager Beer 330 ml | unbranded | branded | 0.9997 |
| Basil | vegetables | unbranded | 0.9997 |
| VKL- Peri Peri Marinade 1Kg | unbranded | branded | 0.9997 |
| Prepit Hyderabad Biriyan 1 kg | unbranded | branded | 0.9996 |
| #_# FC - Orange Popsicle Ice Cream [70 Ml] - Noto | unbranded | branded | 0.9996 |
| TASKI R3 | unbranded | branded | 0.9996 |
| 3 EASTMADE - BLACK PAPER WHOLE (KALI MIRCH) | unbranded | branded | 0.9996 |
| Butter Murkku | unbrand | unbranded | 0.9996 |
| #_# Mango Biscoff Tub - Sassy Teaspoon | unbranded | branded | 0.9996 |
| SCOTCH BRITE - SOFT SPONGE | unbranded | branded | 0.9996 |
| GK-Morde - Hazelnut Chocopaste 1 Kg 140027 | outlet | branded | 0.9996 |
| Lemon Leaves Fresh | unbrand | unbranded | 0.9996 |
| Chefs Art - Piri Piri Sprinkler 250 gm 51189 | outlet | branded | 0.9996 |
| #_# Baked Salted Caramel Cheesecake - Sassy Teaspoon | unbranded | branded | 0.9996 |
| Kissan Tomato Sause Dip | unbranded | branded | 0.9996 |
| SAUCE SOYA DARK | chings | unbranded | 0.9996 |
| #_# Sweet Chilli Sauce 15g - Prasuma | unbranded | branded | 0.9996 |
| Tape 1 Inch | krispy kreme | unbranded | 0.9996 |
| COOKIES JAR WITH LID (46 Pcs) | cremica | unbranded | 0.9996 |
| #_# Cheese (Melted) - Prasuma | unbranded | branded | 0.9996 |
| Silver Pouch | unbrand | unbranded | 0.9996 |
| PASSION FRUIT SYRUP(1 LTR) Foodoo | nutaste | branded | 0.9995 |
| Corn Flour | golden crown | unbranded | 0.9995 |
| HARPIC LIQUID | ovenfresh | branded | 0.9995 |
| #_# The Godfather (Reeses peanut butter cup) Cookie Dough - Cookie Cartel | unbranded | branded | 0.9995 |
| BESAN | rajdhani | unbranded | 0.9995 |
| Mixed Veg Pickle (5 kg)-Snacc | unbranded | branded | 0.9995 |
| Skimmed Milk Powder (SMP) (Milk Protein - 36 percent) | smruti | unbranded | 0.9995 |
| Multi Fold Tissue | outlet | unbranded | 0.9995 |
| PAPER CARRY BAG | ovenfresh | unbranded | 0.9995 |
| Baked Beans 415 Gm | heinz beanz | unbranded | 0.9995 |
| Sesame Seeds White | habit | unbranded | 0.9995 |
| Chilly Byadagi | unbrand | unbranded | 0.9995 |
| Sandburgs Truffle Barbeque sauce (500 gram) | base kitchen | branded | 0.9995 |
| MOTICHOOR LADDU 500g | ksheer sagar | unbranded | 0.9995 |
| #_# Cube Pouches - Entisi Chocolatier | unbranded | branded | 0.9995 |
| Colin (Glass Cleaner) | unbranded | branded | 0.9995 |
| Camino Real Gold 750Ml | unbrand | branded | 0.9994 |
| Fryola Oil | unbranded | branded | 0.9994 |
| Water Bottle Mrp 70 | krispy kreme | unbranded | 0.9994 |
| Cumin Powder | mdh | unbranded | 0.9994 |
| White Raddish | unbrand | unbranded | 0.9994 |
| Monin Blue Curaco 700 ml | unbranded | branded | 0.9994 |
| Shower Gel 5Ltr | unbrand | unbranded | 0.9994 |
| Shudh Garhwal - Khoya Pindi 1KG | unbranded | branded | 0.9993 |
| Fried Mirchi retort | me | unbranded | 0.9993 |
| SAUCE MAYONNAISE | cremica | unbranded | 0.9993 |
| SDU Deva Chardonnay White wine 750ml | unbranded | branded | 0.9993 |
| Grated mozzarella New Onesta | olio | branded | 0.9993 |
| MOTICHOOR LADDU 250g | ksheer sagar | unbranded | 0.9993 |
| GK - Infinite Food - Strawberry Smoothie Premix Powder (58 G x 15 sachet) | outlet | branded | 0.9993 |
| DAILY FRESH SPROUTED PESARATTU BATTER POUCH 1/2KG | wvf | branded | 0.9993 |
| #_# Naga Chilli Sauce - Prasuma | unbranded | branded | 0.9993 |
| Butter Scotch DF Bite | unbranded | branded | 0.9992 |
| #_# Box of 20 Assorted Ganaches - La Folie | unbranded | branded | 0.9992 |
| #_# Hazelnut Mousse Cake [500 gms] [Gluten Free] - Sassy Teaspoon | unbranded | branded | 0.9992 |
| Blue Pine Artesian Water - 750 ML - GST @18 % | unbranded | branded | 0.9992 |
| Grover Selecte Chenin Blanc 750 Ml | unbranded | branded | 0.9992 |
| Burger Box | gfb branded | unbranded | 0.9992 |
| Air Freshener Godrej | unbranded | branded | 0.9992 |
| Parry Sugar White | unbranded | branded | 0.9992 |
| Whole Wheat Penne Pasta | - | unbranded | 0.9992 |
| Nutrela (1pkt) | unbranded | branded | 0.9992 |
| HARPIC | unbranded | branded | 0.9991 |
| Leeks | unbrand | unbranded | 0.9991 |
| Red Raddish | unbrand | unbranded | 0.9991 |
| Whole Wheat Jumbo Bread | cfi | unbranded | 0.9991 |
| J and B Rare | unbranded | branded | 0.9991 |
| Soda Kinley | all brands | branded | 0.9991 |
| Paper Straw | unbrand | unbranded | 0.9991 |
| Cambro Polycarbonate LID for GN Pan 1/1 | unbranded | branded | 0.9991 |
| VKL PERI PERI MARINADE | unbranded | branded | 0.9990 |
| Real Pineapple Juice | unbranded | branded | 0.9990 |
| #_# French Vanilla (100 ml) - Go Zero | unbranded | branded | 0.9990 |
| Cookies Caramel 6kg ( Mec3-14772) | unbranded | branded | 0.9990 |
| Sesame Oil 650 Ml | unbrand | unbranded | 0.9990 |
| Hydrochloric Acid | unbrand | unbranded | 0.9990 |
| #_# PMK Veg Hakka Noodles 250gm - Prasuma | unbranded | branded | 0.9989 |
| White Envelope Cover | unbrand | unbranded | 0.9989 |
| Blueberry Cheesecake Jar | gaw | unbranded | 0.9989 |
| Goat Cheese | flanders daily products | unbranded | 0.9989 |
| Sumabrite Degreaser nd Heavy duty cleaner (break up HD) | unbranded | branded | 0.9988 |
| Teqila Blanco Don Angel 750 Ml | unbrand | branded | 0.9988 |
| EVD DAIRY WHITENER 1 KG | unbranded | branded | 0.9988 |
| RED PAPRIKA SLICED -840 GM | delmonte/frutin /entr%ufffde | unbranded | 0.9988 |
| Oregano Herbs (Seasoning ) | all brands | unbranded | 0.9988 |
| Dosa Rice | unbrand | unbranded | 0.9988 |
| Crispy Chicken Wings- Drums+Flats | olio | unbranded | 0.9988 |
| #_# Kulfi Insulation Bag - Parsi Dairy Farm | unbranded | branded | 0.9988 |
| #_# Sugar Free Chocolate Hazelnut Ice Cream Tub (125 ml) - Bina | unbranded | branded | 0.9987 |
| DAILY FRESH MILLETS IDLI AND DOSA BATTER POUCH 1/2KG | wvf | branded | 0.9987 |
| Chipotle Sauce | timmys | unbranded | 0.9987 |
| Frozen orange | gaw | unbranded | 0.9987 |
| Pesto Hummus 95gm | cfi | unbranded | 0.9986 |
| RTE-Seths - Chinese Ready Schezwan Sauce (Frozen), 1 Kg BB0009 | outlet | branded | 0.9986 |
| SABUDANA NYLON | shri varalakshmi | unbranded | 0.9985 |
| Garlic Bread Seasoning Powder | all brands | unbranded | 0.9985 |
| Coffee and Chocolate Brookies | outlet | unbranded | 0.9985 |
| SAKURA DRIED SHITAKE MUSHROOM | unbranded | branded | 0.9985 |
| #_# Guava Pop (70 ML) - Noto | unbranded | branded | 0.9983 |
| #_# French Vanilla (500 ml) - Go Zero | unbranded | branded | 0.9983 |
| Ketel One Vodka 750 ml | unbranded | branded | 0.9983 |
| DV Grenadine Syrup 750 ml | unbranded | branded | 0.9983 |
| Mixed Pickle 1 Kg | unbrand | unbranded | 0.9982 |
| Chineese Cabbage | unbrand | unbranded | 0.9982 |
| Infinite - Eggless Choco Lava Cake Premix 1 Kg Ambient 148873 | outlet | branded | 0.9981 |
| #_# Pink Dome Box 1/2 Kg - Sassy Teaspoon | unbranded | branded | 0.9981 |
| Dhania Pudina Chutney-SNACC | unbranded | branded | 0.9980 |
| Frozen Fruit Raspberry | unbrand | unbranded | 0.9980 |
| Chilled Chicken Thigh Boneless 1 kg (Rsons) | outlet | branded | 0.9980 |
| Diversey Spray Bottles | unbranded | branded | 0.9980 |
| APRICOT 200 GM PACK | turkel | unbranded | 0.9980 |
| GK-Miami Waffle Pizza Pkg Box 1PKT 100PC GK Dry 137504 | outlet | branded | 0.9979 |
| Ice Tea Bottle - 250ml | - | unbranded | 0.9979 |
| Knor Aromat Seasoning | unbranded | branded | 0.9979 |
| Rich Whipping Cream Gold | unbranded | branded | 0.9979 |
| Pokchay | unbrand | unbranded | 0.9978 |
| SUGAR SACHET - 5GMS | ovenfresh | unbranded | 0.9978 |
| Ajinomoto (Golden Crown) | unbranded | branded | 0.9977 |
| Chicken Tikka filling-Snacc | unbranded | branded | 0.9977 |
| Walnut whole Super (2 Pcs) | nutraj | unbranded | 0.9977 |
| A-005 Grill and Oven Cleaner ACTON | unbranded | branded | 0.9976 |
| Wonder Wipes | unbranded | branded | 0.9976 |
| Manchurian Balls 500 Gms | m i food | unbranded | 0.9976 |
| Windmill Potato starch | unbranded | branded | 0.9975 |
| Disposable Paper Glass 150 ml Customized Printed Cups 180 GSM Paper | outlet | unbranded | 0.9975 |
| Tawa Roti (7 inch) | zomato hyperpure | unbranded | 0.9974 |
| Gulab Jamun (Wyn) | unbranded | branded | 0.9974 |
| Pitambari 150 gm | unbranded | branded | 0.9974 |
| RICE ADA | aachi- double horse | unbranded | 0.9973 |
| Hair Net | minus 30 | unbranded | 0.9972 |
| SCOTCH BRITE  JUNA | unbranded | branded | 0.9972 |
| Phool Makana | unbrand | unbranded | 0.9972 |
| #_# Caramelo Banditos Dough - Cookie Cartel | unbranded | branded | 0.9972 |
| Royal Challenge | unbranded | branded | 0.9972 |
| #_# Sakura Blossom Gateaux (125 Gms) - Ether | unbranded | branded | 0.9971 |
| GFB Mushroom Patty | unbranded | branded | 0.9971 |
| Cone Blueberry Cheesecake  110 Ml | gaw | unbranded | 0.9971 |
| Sundried Tomatoes in oil | olio | unbranded | 0.9970 |
| Pickle Mixed 5Kgs Jar | unbrand | unbranded | 0.9969 |
| Vanaspati Ghee nature fresh | unbranded | branded | 0.9969 |
| Zucchini Yellow (Premium)  incremental 0.5 10033 | outlet | unbranded | 0.9968 |
| #_# Sugar Free Coffee Almond Ice Cream Tub (125 ml) - Bina | unbranded | branded | 0.9968 |
| Red Paprika Sliced | sarwar | unbranded | 0.9967 |
| #_# Soaked Chia - The Whole Truth | unbranded | branded | 0.9967 |
| Spinach | unbrand | unbranded | 0.9966 |
| Sunflower Oil | priya | unbranded | 0.9966 |
| #_# Tag - Gluten-free Paleo Cookies - Le Four | unbranded | branded | 0.9965 |
| SCOTCH BRITE (4 IN 1) | unbranded | branded | 0.9961 |
| tanquery gin 750 | unbranded | branded | 0.9959 |
| NON-VEG BURGER BUN (1x4) | base kitchen | unbranded | 0.9958 |
| Floor Mat | krispy kreme | unbranded | 0.9956 |
| Filter Coffee Powder | krispy kreme | unbranded | 0.9953 |
| SEED POPPY | khush farm | unbranded | 0.9952 |
| #_# Cassata (110 ml) - Go Zero | unbranded | branded | 0.9951 |
| Broccoli  incremental 0.5 10301 | outlet | unbranded | 0.9950 |
| Oaksmith | unbranded | branded | 0.9949 |
| Tandoori Masala Powder | everest | unbranded | 0.9948 |
| Long Note Book 200 Pgs Chandras SB | unbranded | branded | 0.9948 |
| Cheese Block Processed | olio | unbranded | 0.9947 |
| Maida Kesari Brand 50kgs | unbranded | branded | 0.9946 |
| Chicken Drumstick with Skin - Marinated | semifinished | unbranded | 0.9946 |
| Paper Plate | krispy kreme | unbranded | 0.9946 |
| Hazelnut Brownie Outer Sticker (CBTL) | unbranded | branded | 0.9944 |
| Wooden Cutlery Kit | unbrand | unbranded | 0.9942 |
| STICKERS WVF COLD VARAVRAGE - THINK ORIGINS HAZELNUT COLD FILTER COFFEE FSSAI | wvf | branded | 0.9937 |
| Non Veg Spring Rolls -SNACC | unbranded | branded | 0.9937 |
| #_# Baguette Sourdough - La folie | unbranded | branded | 0.9935 |
| Chana Black | unbrand | unbranded | 0.9931 |
| Butter Chiplet | unbrand | unbranded | 0.9930 |
| GK-NY Pan Cake Sp Pkg Box 1PKT 100PC GK Dry 137497 | outlet | branded | 0.9927 |
| #_# Sticker - Mango Protein Smoothie - The Whole Truth | unbranded | branded | 0.9924 |
| R.O Water Bottles (20 Ltrs) | water | unbranded | 0.9921 |
| #_# BC - Aam Ice Cream [300ML] - BICO | unbranded | branded | 0.9917 |
| #_# COCO 40% Dark Chocolate - Ether | unbranded | branded | 0.9914 |
| Jain Hing Powder | unbranded | branded | 0.9914 |
| NUTS CASHEW 4PCS | svp's just cashews - jh sree devi's | unbranded | 0.9913 |
| Lemon Ginger Syrup | krispy kreme | unbranded | 0.9912 |
| Sauce Chilli Green Tops | unbranded | branded | 0.9912 |
| #_# Tender Coconut Litchi Ice Pop - Getaway | unbranded | branded | 0.9910 |
| Milkhana Melted Cheese | unbranded | branded | 0.9900 |
| Fine Sev | chaat street | unbranded | 0.9898 |
| Cassata - 125ml | gaw | unbranded | 0.9890 |
| #_# Slide Tru Hamper Box OF 4 Outer - The Tiny Tub | unbranded | branded | 0.9885 |
| #_# Sticker - Sauce Dip Sticker Crunchy Chilli Oil - Prasuma | unbranded | branded | 0.9881 |
| #_# Pista Kulfi Stick (70 ml) - Go Zero | unbranded | branded | 0.9876 |
| Dosa Masala Retort | me | unbranded | 0.9853 |
| ATTA GANGA | unbranded | branded | 0.9853 |
| Chicken Tikka Marinated | oh delhi | unbranded | 0.9843 |
| Scotch Brite - Rubber Kitchen Gloves | scotch brite | branded | 0.9838 |
| SLEEVES 750 ML BAGASSE CATERSPOINT | caterspoint | branded | 0.9836 |
| Kimirica White Gold Tooth Brush pack | unbranded | branded | 0.9833 |
| #_# Black Ceaser Dough - Cookie Cartel | unbranded | branded | 0.9831 |
| Paper Cup 350ml (10'' Oz) FLYP | unbranded | branded | 0.9826 |
| #_# SIERRA 72% Dark Chocolate Bar - Ether | unbranded | branded | 0.9820 |
| #_# Chocolate Fudge Overload (NAS) 500 ml - Frozen Fun | unbranded | branded | 0.9817 |
| #_# Frozen OG Chocolate Chip Chonker - Chonkers | unbranded | branded | 0.9812 |
| Side Box (Crunch) | crunch | unbranded | 0.9809 |
| Wonder Wipe (3pc) | unbranded | branded | 0.9803 |
| #_# Assorted Roleys (Box of 6) - Meemees | unbranded | branded | 0.9790 |
| BREAD COVER 2 | ovenfresh | unbranded | 0.9777 |
| Thondaika | unbrand | unbranded | 0.9777 |
| Chuk Plate 11 | unbranded | branded | 0.9774 |
| Panini Bread Outer Sticker (CBTL) | unbranded | branded | 0.9770 |
| Good Night Machine | unbranded | branded | 0.9756 |
| Dal Tadka Lentils- ( 920 gms ) | cfi | unbranded | 0.9752 |
| #_# Eggless Chocolate Chip Pound Cake - Sweetish | unbranded | branded | 0.9752 |
| Q-com Teacake Blister Tray | cz | branded | 0.9744 |
| TG-Party Snacks 35G Pouch | unbranded | branded | 0.9732 |
| Thai Jasmine Rice 2kg pkt MBK | unbranded | branded | 0.9728 |
| Breakfast Sugar Trust 1 Kg | unbranded | branded | 0.9724 |
| Coconut milk powder maggi | unbranded | branded | 0.9702 |
| Dollur Amla Jar | unbranded | branded | 0.9689 |
| Budweiser Premium | unbranded | branded | 0.9684 |
| GTC Pizza Box 9x9 | unbranded | branded | 0.9679 |
| #_# Double Chocolate Chip Cookie Premix - 8 pcs - Sweetish | unbranded | branded | 0.9674 |
| EGG FREE RED VELVET CAKE MIX | ovenfresh | branded | 0.9669 |
| LAVA CAKE LID | ovenfresh | unbranded | 0.9664 |
| QT Rail | unbranded | branded | 0.9659 |
| #_# Container lid - PMK Round Paper 500 ML Plastic - Prasuma | unbranded | branded | 0.9649 |
| Finagel | unbranded | branded | 0.9615 |
| Lotus Flour | unbranded | branded | 0.9610 |
| Cello Tape 1 | unbrand | branded | 0.9560 |
| #_# Kesar Peda 500gms - Genda Phool | unbranded | branded | 0.9546 |
| SP Thundercrush French Fries 9mm | unbranded | branded | 0.9540 |
| #_# Sticker - Momo Kitchen 40mm - Prasuma | unbranded | branded | 0.9533 |
| #_# Greeting Card - Sassy Teaspoon | unbranded | branded | 0.9504 |
| #_# XYLITOL Chocolate Hazelnut Icecream (600ML) - Bina | unbranded | branded | 0.9504 |
| Sriracha (570gm bottle) | unbranded | branded | 0.9474 |
| Malai Paneer Soft Loose | shreeji dairy | unbranded | 0.9466 |
| #_# Square Butter Paper - Le Four | unbranded | branded | 0.9450 |
| Heeng Papdi 200g | ksheer sagar | unbranded | 0.9372 |
| Black and White 750Ml | unbrand | branded | 0.9363 |
| Keora Water 500Ml | unbrand | unbranded | 0.9344 |
| Mother's Day Double Chocolate Brownie box - Blinkit / Instamart | cz | unbranded | 0.9263 |
| AACHI KULAMBU MILAKAI STAFF | ovenfresh | branded | 0.9241 |
| #_# Cone - Dark Chocolate [ 120 ml ] - Getaway | unbranded | branded | 0.9219 |
| #_# Griselda's Red Velvet Sticker (Eggless) - Cookie Cartel | unbranded | branded | 0.9196 |
| TOP COVER OF BOX 750 ML SALADSPOINT | unbranded | branded | 0.9185 |
| Plum Essence | unbranded | branded | 0.9099 |
| Economy - Staff Toor Dal 1 Kg (Non IP) 131965 | outlet | branded | 0.8991 |
| Outer Bag SOS 70 GSM - Snacc | unbranded | branded | 0.8977 |
| Tea flask - 250 ML -Outer coorugated Box-Snacc | unbranded | branded | 0.8903 |
| MANGO JUICE 1 LTR | unbranded | branded | 0.8903 |
| #_# Tango Mango - Anando | unbranded | branded | 0.8634 |
| PERFECT NO-BAKE CHEESECAKE MIX (1KG) | unbranded | branded | 0.8539 |
| MINI JAMUN 100g | ksheer sagar | unbranded | 0.8539 |
| Termocool morded box | unbranded | branded | 0.8520 |
| 11.5x11.5 (Round) Sandhouse Butter paper (40GSM) | unbranded | branded | 0.8397 |
| #_# Baked Oregano Cheese Matthi - Genda Phool | unbranded | branded | 0.8199 |
| 110 Ml Tea paper cup-Snacc | unbranded | branded | 0.8199 |
| Ciclo Printed Cake Box 2Pc | unbranded | branded | 0.8176 |
| GLUTEN NB 0121 | unbranded | branded | 0.8129 |
| Fruit Filling Mango Delta | unbranded | branded | 0.8056 |
| Cutlery Set The Cake Story | unbranded | branded | 0.7905 |
| #_# Caramelo Banditos Sticker - Cookie Cartel | unbranded | branded | 0.7905 |
| CELLO TAPE BIG PLAIN 3 INCH | unbranded | branded | 0.7905 |
| Crispy Cajun Breading Mix | unbrand | branded | 0.7879 |
| #_# Hamper Box Of 2 Outer  - The Tiny Tub | unbranded | branded | 0.7853 |
| Star Papad | unbranded | branded | 0.7827 |
| Butter Croissant-Snacc | unbranded | branded | 0.7827 |
| #_# Wooden Spoon - Amore | unbranded | branded | 0.7773 |
| San Marzano - Pomace Olive Oil | san marzano | branded | 0.7746 |
| #_# Frozen Chonk O Rocher - Chonkers | unbranded | branded | 0.7718 |
| Triplesec | unbranded | branded | 0.7663 |
| CELLOFIN PAPER | unbranded | branded | 0.7578 |
| MF White Compound CO W33 | unbranded | branded | 0.7372 |
| Mogra Staff Rice (Broken Basmati Rice) 30 Kg 138777 | outlet | unbranded | 0.7280 |
| #_# Big Blue Box - Sweetish | unbranded | branded | 0.7249 |
| Ajinomato | unbranded | branded | 0.7154 |
| Gochujang 17kg Tin | unbranded | branded | 0.7058 |
| Timmys Food Bag | unbranded | branded | 0.6619 |
| Kcco Tray Big | unbranded | branded | 0.6406 |
| ONION RINGS (PB) | olio | unbranded | 0.6406 |
| MRD Stickers | unbranded | branded | 0.6370 |
| Classic Ice Burst 10 Nos | unbrand | branded | 0.5312 |
| Kiley Soda 250 ML - SNACC | unbranded | branded | 0.5273 |
| Chlorin Liquid | unbrand | branded | 0.5234 |
| NONBROMITE BREAD IMPROVER 1 KG 0157 | unbranded | branded | 0.5117 |
| HOLLO MAT3125*5 | unbranded | branded | 0.5078 |
| Napkin Bikkgane | unbranded | branded | 0.5078 |
| Softy Premix Vanilla | minus 30 | branded | 0.5000 |
| Iceberg | unbrand | unbranded | 0.5000 |
| Plain Container - Classic Cassata (110 ml) | unbranded | branded | 0.5000 |
| Milk Compound Slab M21 | unbranded | branded | 0.4844 |
| Nam Shop Sticker   Prawn Crackers Large | unbranded | branded | 0.4805 |
| #_# Cacao Crispy - Ether | unbranded | branded | 0.4649 |
| #_# Sticker - Sauce Dip Sticker Tangy Thai Tom Yum Sauce - Prasuma | unbranded | branded | 0.4610 |
| BANARASI LAL PEDA-200 Gms | ksheer sagar | branded | 0.4494 |
| PG-Paper Tub Lids | unbranded | branded | 0.4111 |
| Fruit Cocktail Tin | unbranded | branded | 0.3998 |
| UCC 2door 3drawer + raised BM + 1/6gnx6 | custom | branded | 0.3812 |
| Food Colours Splash 200g Assorted | unbranded | branded | 0.3702 |
| YU001517 Sensor Magnetiv 2 Nc | unbranded | branded | 0.3277 |
| Golden Dust | unbranded | branded | 0.3141 |
| TT RIBBAN J304 (110MM X 300MTR) | unbranded | branded | 0.2814 |
| SAMSEER MARK | unbranded | branded | 0.2568 |
| Vanaspati 1kg pkt | unbranded | branded | 0.2539 |
| STICKER SALAD | unbranded | branded | 0.2509 |
| Twinning Lemon Tea | unbrand | branded | 0.2451 |
| Keto Blueberry Cheesecake Ice Cream - 100 ml RM | gaw | branded | 0.2422 |
| ROSE MARY | unbranded | branded | 0.2309 |
| #_# Cothas Blend Coffee 200 Gm - Murukku | unbranded | branded | 0.2309 |
| Hand Sanitizer HS 100 | unbranded | branded | 0.2227 |
| #_# Jar - Death By Chocolate - Getaway | unbranded | branded | 0.2200 |
| Chocolate Hamper 812 | unbranded | branded | 0.2121 |
| 2 Cp-Snacc | unbranded | branded | 0.1824 |
| Sambal Oelek | unbranded | branded | 0.1711 |
| Cotton BBK Apron | unbranded | branded | 0.1711 |
| Sipper Cup 300ml | thee pacakging co | unbranded | 0.1711 |
| AANCH COVER | unbranded | branded | 0.1689 |
| TL Hitachi UX Makeup 800ml | unbranded | branded | 0.1624 |
| Zukni Green | unbranded | branded | 0.1259 |
| Topper | unbranded | branded | 0.1176 |
| MINERAL WATER BOTTLE 1 LIT SF | unbranded | branded | 0.1128 |
| MUMBAI RAVA 5 KG | unbranded | branded | 0.1097 |
| ROW - Barcode Lable 50mmX25mm Non Tearable | unbranded | branded | 0.0981 |
| TL Slicer Cutter | unbranded | branded | 0.0981 |
| Sweets Milk Barfi Red Velvet | unbranded | branded | 0.0940 |
| HING (LG) | unbranded | branded | 0.0888 |
| Mozzarella Cheese - Flanders | unbranded | branded | 0.0770 |
| Tom Kha Paste 1kg pkt | unbranded | branded | 0.0706 |
| EGGFREE TEA TIME VANILLA MUFFIN | unbranded | branded | 0.0685 |
| Luster Dust Royal Gold | unbranded | branded | 0.0534 |
| Chocolate Hamper 1864 | unbranded | branded | 0.0434 |
| Kung Pao Sauce 335 G | unbranded | branded | 0.0357 |
| Chef Coat S36  Black Half Sleeve | unbranded | branded | 0.0357 |
| Dark Chocolate Paste-NAS | unbranded | branded | 0.0351 |
| COLOUR CODE DOTT TUES | unbranded | branded | 0.0331 |
| #_# Big Bag - Stroopie | unbranded | branded | 0.0331 |
| BARDINET BRANDY 1000 ML | unbranded | branded | 0.0326 |
| Flow Wrap Rolls - Raspberry Duet (60 ml) | unbranded | branded | 0.0316 |
| Ro 48 | unbranded | branded | 0.0260 |
| Quarry And Tile Floor Cleaner (120X2Oz) | krispy kreme | branded | 0.0230 |
| Sticker Mutton Haleem | unbranded | branded | 0.0213 |
| Texmex cheese sauce | unbranded | branded | 0.0180 |
| InWard Register | unbranded | branded | 0.0177 |
| DESERT SPOON 12GTIDY | unbranded | branded | 0.0122 |
| CHULLA | unbranded | branded | 0.0119 |
| Kesar Kaju Katli 500 Gms Gold Foil Cover | unbranded | branded | 0.0081 |
| Canteen Drink Box (250GSM) SBS | unbranded | branded | 0.0065 |
| STICKER SHEEK KABAB | unbranded | branded | 0.0041 |
| Millet Dosa Batter - ME | me | branded | 0.0038 |
| COKE CANE | unbranded | branded | 0.0027 |
| TORCH BLOW COOKING | unbranded | branded | 0.0020 |
| XO Sauce Sticker | unbranded | branded | 0.0015 |
| Newyork Cheese Filling | krispy kreme | branded | 0.0015 |
| Aampanna juice 150ml | unbranded | branded | 0.0014 |
| #_# Gate Pass Book | unbranded | branded | 0.0012 |
| Pizza Platter Butter Paper 16*9 | unbranded | branded | 0.0010 |
| SS Mould Round Cutter - 12pcs | unbranded | branded | 0.0009 |
| Cmc Powder | unbranded | branded | 0.0005 |
| Danish White Feta 500GM | unbranded | branded | 0.0005 |
| SS  NOODAL CHANNI | unbranded | branded | 0.0004 |
| Cake Saver | unbranded | branded | 0.0003 |
| Bandan Cap | unbranded | branded | 0.0003 |
| N20 Whipped Cream Chargers | unbranded | branded | 0.0002 |
| SS GN PAN 1/3 100 MM | unbranded | branded | 0.0001 |
| Boba Lychee can | unbranded | branded | 0.0001 |
| Truffle Paste (500gm Pack) | unbranded | branded | 0.0001 |
| FRENCH HEARTS VINYL STICKER SET | unbranded | branded | 0.0000 |

## Per-row detail

| title | true | pred | P(branded) | confidence |
|---|---|---|---|---|
| Ketchup | — | unbranded | n/a | 0.9992 |
| 3CP PLATE | — | unbranded | n/a | 0.9998 |
| Cayenne Pepper Powder | — | unbranded | n/a | 0.9996 |
| Dark Compound Co D15 500Gms | — | branded | n/a | 0.2282 |
| Staff Mustard Whole | — | unbranded | n/a | 0.3007 |
| Garbage Bag Big 30X50 Virgin | — | unbranded | n/a | 0.9997 |
| Green Chillies | — | unbranded | n/a | 0.9999 |
| Maraschino Cherry 737 Gms | — | unbranded | n/a | 0.9962 |
| Cashewnuts | — | unbranded | n/a | 0.9951 |
| Basa Fish | — | unbranded | n/a | 0.9997 |
| CHICKEN FRY MIXTURE (CF1) | — | unbranded | n/a | 0.9885 |
| Kashmir Chili Whole | — | unbranded | n/a | 0.9987 |
| CAPSICUM - Green | — | unbranded | n/a | 0.9998 |
| Chops | — | unbranded | n/a | 0.9252 |
| Gochujang Sauce | — | unbranded | n/a | 0.9979 |
| coke 250ml bgl entperises aahar sale (Pack of 28) | — | branded | n/a | 0.9988 |
| MDH Pav Bhaji Masala 100 grams | — | branded | n/a | 1.0000 |
| Hungritos Permium without Skin On Fries 9Mm | — | branded | n/a | 0.9989 |
| Chick peas | — | unbranded | n/a | 0.9986 |
| Pork Red Meat | — | unbranded | n/a | 0.9989 |
| MDH Kashmiri Chilli Powder 100 grams | — | branded | n/a | 1.0000 |
| Coca Cola 180ML (Pack of 36PCS) | — | branded | n/a | 1.0000 |
| Light Soya Sauce | — | unbranded | n/a | 0.9994 |
| Wet Wipes | — | unbranded | n/a | 0.9985 |
| Tastecraft Pistachio Flavoured Syrup 750ml | — | branded | n/a | 0.9996 |
| Tandoori Tikka Masala | — | unbranded | n/a | 0.9954 |
| Brown Packing Tape 2 Inch | — | unbranded | n/a | 1.0000 |
| Ice Tea Bottle - 250ml ⚠ | - | unbranded | n/a | 0.9979 |
| Whole Wheat Penne Pasta ⚠ | - | unbranded | n/a | 0.9992 |
| RICE ADA ⚠ | aachi- double horse | unbranded | n/a | 0.9973 |
| AASHIRVAAD - ATTA 10 KG BAG ⚠ | aashirvaad | branded | n/a | 1.0000 |
| Coriander Fresh W/O Roots ⚠ | all brands | unbranded | n/a | 0.9997 |
| Oregano Herbs (Seasoning ) ⚠ | all brands | unbranded | n/a | 0.9988 |
| Soda Kinley ⚠ | all brands | branded | n/a | 0.9991 |
| Pickle Sachet ⚠ | all brands | unbranded | n/a | 0.9999 |
| Garlic Bread Seasoning Powder ⚠ | all brands | unbranded | n/a | 0.9985 |
| MILK AMUL TETRA PACK ⚠ | amul | branded | n/a | 1.0000 |
| ANANDA PANEER 1 KG ⚠ | ananda | branded | n/a | 1.0000 |
| Almond biscotti (1pcs) ⚠ | base kitchen | unbranded | n/a | 0.9998 |
| NON-VEG BURGER BUN (1x4) ⚠ | base kitchen | unbranded | n/a | 0.9958 |
| CHOCOLATE GANACHE (500GM) ⚠ | base kitchen | unbranded | n/a | 0.9997 |
| Sandburgs Truffle Barbeque sauce (500 gram) ⚠ | base kitchen | branded | n/a | 0.9995 |
| SLEEVES 750 ML BAGASSE CATERSPOINT ⚠ | caterspoint | branded | n/a | 0.9836 |
| Whole Wheat Jumbo Bread ⚠ | cfi | unbranded | n/a | 0.9991 |
| Pesto Hummus 95gm ⚠ | cfi | unbranded | n/a | 0.9986 |
| Dal Tadka Lentils- ( 920 gms ) ⚠ | cfi | unbranded | n/a | 0.9752 |
| MTR Sambar ⚠ | cfi | branded | n/a | 1.0000 |
| Fine Sev ⚠ | chaat street | unbranded | n/a | 0.9898 |
| SAUCE SOYA DARK ⚠ | chings | unbranded | n/a | 0.9996 |
| Coke Can 300 Ml ⚠ | coca cola | branded | n/a | 1.0000 |
| Thums Up 250 ml ⚠ | coke | branded | n/a | 0.9998 |
| Beer Non Alcoholic 330 ml - Coolberg (Ginger Flavour) ⚠ | coolberg | branded | n/a | 0.9998 |
| SAUCE MAYONNAISE ⚠ | cremica | unbranded | n/a | 0.9993 |
| COOKIES JAR WITH LID (46 Pcs) ⚠ | cremica | unbranded | n/a | 0.9996 |
| Side Box (Crunch) ⚠ | crunch | unbranded | n/a | 0.9809 |
| UCC 2door 3drawer + raised BM + 1/6gnx6 ⚠ | custom | branded | n/a | 0.3812 |
| Griffith Hot Chilli Marinade ⚠ | custom culinary | branded | n/a | 0.9998 |
| Mother's Day Double Chocolate Brownie box - Blinkit / Instamart ⚠ | cz | unbranded | n/a | 0.9263 |
| Q-com Teacake Blister Tray ⚠ | cz | branded | n/a | 0.9744 |
| Delmonte - Eggless Mayo ⚠ | delmonte | branded | n/a | 0.9999 |
| RED PAPRIKA SLICED -840 GM ⚠ | delmonte/frutin /entr%ufffde | unbranded | n/a | 0.9988 |
| Taski R7 - 5ltr Can ⚠ | diversey | branded | n/a | 0.9999 |
| PLASTIC CONTAINER 750ML ⚠ | divya | unbranded | n/a | 0.9998 |
| Tandoori Masala Powder ⚠ | everest | unbranded | n/a | 0.9948 |
| Goat Cheese ⚠ | flanders daily products | unbranded | n/a | 0.9989 |
| Cassata - 125ml ⚠ | gaw | unbranded | n/a | 0.9890 |
| Keto Blueberry Cheesecake Ice Cream - 100 ml RM ⚠ | gaw | branded | n/a | 0.2422 |
| Blueberry Cheesecake Jar ⚠ | gaw | unbranded | n/a | 0.9989 |
| Cone Blueberry Cheesecake  110 Ml ⚠ | gaw | unbranded | n/a | 0.9971 |
| Frozen orange ⚠ | gaw | unbranded | n/a | 0.9987 |
| Burger Box ⚠ | gfb branded | unbranded | n/a | 0.9992 |
| Corn Flour ⚠ | golden crown | unbranded | n/a | 0.9995 |
| Sesame Seeds White ⚠ | habit | unbranded | n/a | 0.9995 |
| Baked Beans 415 Gm ⚠ | heinz beanz | unbranded | n/a | 0.9995 |
| PLASTIC CONTAINER 25ML ⚠ | ice packing | unbranded | n/a | 0.9998 |
| DRY COCONUT ⚠ | jay maruthi gold | unbranded | n/a | 0.9997 |
| SEED POPPY ⚠ | khush farm | unbranded | n/a | 0.9952 |
| Lemon Ginger Syrup ⚠ | krispy kreme | unbranded | n/a | 0.9912 |
| Water Bottle Mrp 70 ⚠ | krispy kreme | unbranded | n/a | 0.9994 |
| Quarry And Tile Floor Cleaner (120X2Oz) ⚠ | krispy kreme | branded | n/a | 0.0230 |
| Floor Mat ⚠ | krispy kreme | unbranded | n/a | 0.9956 |
| Shot Glass 60Ml ⚠ | krispy kreme | unbranded | n/a | 0.9997 |
| Tape 1 Inch ⚠ | krispy kreme | unbranded | n/a | 0.9996 |
| Filter Coffee Powder ⚠ | krispy kreme | unbranded | n/a | 0.9953 |
| Newyork Cheese Filling ⚠ | krispy kreme | branded | n/a | 0.0015 |
| Paper Plate ⚠ | krispy kreme | unbranded | n/a | 0.9946 |
| BANARASI LAL PEDA-200 Gms ⚠ | ksheer sagar | branded | n/a | 0.4494 |
| Heeng Papdi 200g ⚠ | ksheer sagar | unbranded | n/a | 0.9372 |
| MOTICHOOR LADDU 250g ⚠ | ksheer sagar | unbranded | n/a | 0.9993 |
| MINI JAMUN 100g ⚠ | ksheer sagar | unbranded | n/a | 0.8539 |
| MOTICHOOR LADDU 500g ⚠ | ksheer sagar | unbranded | n/a | 0.9995 |
| Manchurian Balls 500 Gms ⚠ | m i food | unbranded | n/a | 0.9976 |
| Cumin Powder ⚠ | mdh | unbranded | n/a | 0.9994 |
| Dosa Masala Retort ⚠ | me | unbranded | n/a | 0.9853 |
| Fried Mirchi retort ⚠ | me | unbranded | n/a | 0.9993 |
| Millet Dosa Batter - ME ⚠ | me | branded | n/a | 0.0038 |
| Softy Premix Vanilla ⚠ | minus 30 | branded | n/a | 0.5000 |
| Hair Net ⚠ | minus 30 | unbranded | n/a | 0.9972 |
| MONIN VANILLA SYRUP 1 L ⚠ | monin | branded | n/a | 1.0000 |
| RICE DOSA ⚠ | nandi-sln-a1 | unbranded | n/a | 0.9998 |
| PASSION FRUIT SYRUP(1 LTR) Foodoo ⚠ | nutaste | branded | n/a | 0.9995 |
| Walnut whole Super (2 Pcs) ⚠ | nutraj | unbranded | n/a | 0.9977 |
| Chicken Tikka Marinated ⚠ | oh delhi | unbranded | n/a | 0.9843 |
| Crispy Chicken Wings- Drums+Flats ⚠ | olio | unbranded | n/a | 0.9988 |
| Sundried Tomatoes in oil ⚠ | olio | unbranded | n/a | 0.9970 |
| Chicken wings Coated ( ITC ) ⚠ | olio | branded | n/a | 0.9999 |
| Coca cola 750ml ⚠ | olio | branded | n/a | 1.0000 |
| Grated mozzarella New Onesta ⚠ | olio | branded | n/a | 0.9993 |
| Cheese Block Processed ⚠ | olio | unbranded | n/a | 0.9947 |
| ONION RINGS (PB) ⚠ | olio | unbranded | n/a | 0.6406 |
| GK-NY Pan Cake Sp Pkg Box 1PKT 100PC GK Dry 137497 ⚠ | outlet | branded | n/a | 0.9927 |
| Malaysian Noodles ( Flat Noodles ) 1kg ⚠ | outlet | unbranded | n/a | 0.9998 |
| Carrots/Gajar, incremental 0.5 10335 ⚠ | outlet | unbranded | n/a | 0.9998 |
| Zucchini Yellow (Premium)  incremental 0.5 10033 ⚠ | outlet | unbranded | n/a | 0.9968 |
| Infinite - Eggless Choco Lava Cake Premix 1 Kg Ambient 148873 ⚠ | outlet | branded | n/a | 0.9981 |
| Lobo - 5 Spice Powder 65 gm 51547 ⚠ | outlet | branded | n/a | 0.9999 |
| GK-Morde - Hazelnut Chocopaste 1 Kg 140027 ⚠ | outlet | branded | n/a | 0.9996 |
| Chef's Art - Crispy Cajun Breading Mix 1 Kg H51176 ⚠ | outlet | branded | n/a | 0.9998 |
| GK-Miami Waffle Pizza Pkg Box 1PKT 100PC GK Dry 137504 ⚠ | outlet | branded | n/a | 0.9979 |
| MDH - White Pepper Powder 100 gm 30291 ⚠ | outlet | branded | n/a | 1.0000 |
| Multi Fold Tissue ⚠ | outlet | unbranded | n/a | 0.9995 |
| Chefs Art - Jamaican Jerk Seasoning 400 gm ⚠ | outlet | branded | n/a | 0.9997 |
| Chilled Chicken Thigh Boneless 1 kg (Rsons) ⚠ | outlet | branded | n/a | 0.9980 |
| Chefs Art - Piri Piri Sprinkler 250 gm 51189 ⚠ | outlet | branded | n/a | 0.9996 |
| Economy - Staff Toor Dal 1 Kg (Non IP) 131965 ⚠ | outlet | branded | n/a | 0.8991 |
| Newtrition - Lemon Ginger, 500 ML ⚠ | outlet | branded | n/a | 0.9998 |
| Disposable Paper Glass 150 ml Customized Printed Cups 180 GSM Paper ⚠ | outlet | unbranded | n/a | 0.9975 |
| Mogra Staff Rice (Broken Basmati Rice) 30 Kg 138777 ⚠ | outlet | unbranded | n/a | 0.7280 |
| GK - Infinite Food - Strawberry Smoothie Premix Powder (58 G x 15 sachet) ⚠ | outlet | branded | n/a | 0.9993 |
| Coffee and Chocolate Brookies ⚠ | outlet | unbranded | n/a | 0.9985 |
| RTE-Seths - Chinese Ready Schezwan Sauce (Frozen) 1 Kg ⚠ | outlet | branded | n/a | 0.9997 |
| Aluminium (Silver) Pouches 6 inch * 9 inch (Pack of 100) 137302 ⚠ | outlet | unbranded | n/a | 0.9998 |
| RTE-Seths - Chinese Ready Schezwan Sauce (Frozen), 1 Kg BB0009 ⚠ | outlet | branded | n/a | 0.9986 |
| Broccoli  incremental 0.5 10301 ⚠ | outlet | unbranded | n/a | 0.9950 |
| 340 MM BOPP ROLL ⚠ | ovenfresh | unbranded | n/a | 0.9998 |
| HARPIC LIQUID ⚠ | ovenfresh | branded | n/a | 0.9995 |
| BREAD COVER 2 ⚠ | ovenfresh | unbranded | n/a | 0.9777 |
| PAPER CARRY BAG ⚠ | ovenfresh | unbranded | n/a | 0.9995 |
| SANDWICH BOX ⚠ | ovenfresh | unbranded | n/a | 0.9999 |
| SUGAR SACHET - 5GMS ⚠ | ovenfresh | unbranded | n/a | 0.9978 |
| AACHI KULAMBU MILAKAI STAFF ⚠ | ovenfresh | branded | n/a | 0.9241 |
| LAVA CAKE LID ⚠ | ovenfresh | unbranded | n/a | 0.9664 |
| EGG FREE RED VELVET CAKE MIX ⚠ | ovenfresh | branded | n/a | 0.9669 |
| SPRITE 250ML ⚠ | pepsi | branded | n/a | 1.0000 |
| Possmei Taro Powder Premix 1kg pkt ⚠ | possmei | branded | n/a | 0.9999 |
| Possmei Passion Fruit Syrup 2.5Kg bottle ⚠ | possmei | branded | n/a | 0.9999 |
| Sunflower Oil ⚠ | priya | unbranded | n/a | 0.9966 |
| BESAN ⚠ | rajdhani | unbranded | n/a | 0.9995 |
| Orange Juice 1 Lltr ⚠ | real | unbranded | n/a | 0.9998 |
| San Marzano - Pomace Olive Oil ⚠ | san marzano | branded | n/a | 0.7746 |
| Red Paprika Sliced ⚠ | sarwar | unbranded | n/a | 0.9967 |
| Scotch Brite - Rubber Kitchen Gloves ⚠ | scotch brite | branded | n/a | 0.9838 |
| Chicken Drumstick with Skin - Marinated ⚠ | semifinished | unbranded | n/a | 0.9946 |
| Malai Paneer Soft Loose ⚠ | shreeji dairy | unbranded | n/a | 0.9466 |
| Shresth Gold Milk 500 Ml ⚠ | shreeji dairy | branded | n/a | 0.9999 |
| SABUDANA NYLON ⚠ | shri varalakshmi | unbranded | n/a | 0.9985 |
| Skimmed Milk Powder (SMP) (Milk Protein - 36 percent) ⚠ | smruti | unbranded | n/a | 0.9995 |
| NUTS CASHEW 4PCS ⚠ | svp's just cashews - jh sree devi's | unbranded | n/a | 0.9913 |
| Sipper Cup 300ml ⚠ | thee pacakging co | unbranded | n/a | 0.1711 |
| Chipotle Sauce ⚠ | timmys | unbranded | n/a | 0.9987 |
| APRICOT 200 GM PACK ⚠ | turkel | unbranded | n/a | 0.9980 |
| Chana Black ⚠ | unbrand | unbranded | n/a | 0.9931 |
| Crispy Cajun Breading Mix ⚠ | unbrand | branded | n/a | 0.7879 |
| Butter Murkku ⚠ | unbrand | unbranded | n/a | 0.9996 |
| Wooden Cutlery Kit ⚠ | unbrand | unbranded | n/a | 0.9942 |
| Teqila Blanco Don Angel 750 Ml ⚠ | unbrand | branded | n/a | 0.9988 |
| White Envelope Cover ⚠ | unbrand | unbranded | n/a | 0.9989 |
| Leeks ⚠ | unbrand | unbranded | n/a | 0.9991 |
| Classic Ice Burst 10 Nos ⚠ | unbrand | branded | n/a | 0.5312 |
| Red Raddish ⚠ | unbrand | unbranded | n/a | 0.9991 |
| Camino Real Gold 750Ml ⚠ | unbrand | branded | n/a | 0.9994 |
| Sesame Oil 650 Ml ⚠ | unbrand | unbranded | n/a | 0.9990 |
| Hydrochloric Acid ⚠ | unbrand | unbranded | n/a | 0.9990 |
| Artichoke Tin 390 Grms ⚠ | unbrand | unbranded | n/a | 0.9998 |
| Red Yellow Capsicum Mixed ⚠ | unbrand | unbranded | n/a | 0.9999 |
| Pokchay ⚠ | unbrand | unbranded | n/a | 0.9978 |
| Chlorin Liquid ⚠ | unbrand | branded | n/a | 0.5234 |
| Frozen Fruit Raspberry ⚠ | unbrand | unbranded | n/a | 0.9980 |
| Pickle Mixed 5Kgs Jar ⚠ | unbrand | unbranded | n/a | 0.9969 |
| Phool Makana ⚠ | unbrand | unbranded | n/a | 0.9972 |
| Thondaika ⚠ | unbrand | unbranded | n/a | 0.9777 |
| Tropicana Orange Juice 1 Ltr ⚠ | unbrand | branded | n/a | 1.0000 |
| Dosa Rice ⚠ | unbrand | unbranded | n/a | 0.9988 |
| Spinach ⚠ | unbrand | unbranded | n/a | 0.9966 |
| Mixed Pickle 1 Kg ⚠ | unbrand | unbranded | n/a | 0.9982 |
| 100 Pipers. 750Ml ⚠ | unbrand | branded | n/a | 1.0000 |
| Iceberg ⚠ | unbrand | unbranded | n/a | 0.5000 |
| Butter Paper 15*15 ⚠ | unbrand | unbranded | n/a | 0.9999 |
| Paper Straw ⚠ | unbrand | unbranded | n/a | 0.9991 |
| Keora Water 500Ml ⚠ | unbrand | unbranded | n/a | 0.9344 |
| Lemon Leaves Fresh ⚠ | unbrand | unbranded | n/a | 0.9996 |
| Cello Tape 1 ⚠ | unbrand | branded | n/a | 0.9560 |
| Butter Chiplet ⚠ | unbrand | unbranded | n/a | 0.9930 |
| Green Mustard Microgreen ⚠ | unbrand | unbranded | n/a | 0.9998 |
| Harpic 500 Ml ⚠ | unbrand | branded | n/a | 1.0000 |
| Black and White 750Ml ⚠ | unbrand | branded | n/a | 0.9363 |
| Jacobs Creek Red 750Ml ⚠ | unbrand | branded | n/a | 1.0000 |
| Chilly Byadagi ⚠ | unbrand | unbranded | n/a | 0.9995 |
| Budweiser 330Ml ⚠ | unbrand | branded | n/a | 0.9998 |
| White Raddish ⚠ | unbrand | unbranded | n/a | 0.9994 |
| Cherry Tomato ⚠ | unbrand | unbranded | n/a | 0.9999 |
| Tropicana Mango Juice 1Ltr ⚠ | unbrand | branded | n/a | 1.0000 |
| Onion Sambar ⚠ | unbrand | unbranded | n/a | 0.9997 |
| Chineese Cabbage ⚠ | unbrand | unbranded | n/a | 0.9982 |
| Twinning Lemon Tea ⚠ | unbrand | branded | n/a | 0.2451 |
| Shower Gel 5Ltr ⚠ | unbrand | unbranded | n/a | 0.9994 |
| Silver Pouch ⚠ | unbrand | unbranded | n/a | 0.9996 |
| Monin Peach Syrup ⚠ | unbrand | branded | n/a | 1.0000 |
| HARPIC ⚠ | unbranded | branded | n/a | 0.9991 |
| Sakthi - Kulambu Chilli powder, 500gm ⚠ | unbranded | branded | n/a | 1.0000 |
| EASTMADE - CUMIN (JEERA) 1 KG ⚠ | unbranded | branded | n/a | 0.9998 |
| Chicken Curry Cut | unbranded | unbranded | n/a | 0.9928 |
| Kashmiri Mirch Powder | unbranded | unbranded | n/a | 0.9960 |
| ROW - Barcode Lable 50mmX25mm Non Tearable ⚠ | unbranded | branded | n/a | 0.0981 |
| Silken Tofu 300g Voila ⚠ | unbranded | branded | n/a | 0.9998 |
| T Shirt Black NM M38 | unbranded | unbranded | n/a | 0.9993 |
| Papad ( Big) | unbranded | unbranded | n/a | 0.9995 |
| ROOH AFZA ⚠ | unbranded | branded | n/a | 0.9998 |
| Taski Suma Ultra (L2) 5L Can ⚠ | unbranded | branded | n/a | 1.0000 |
| Eggs | unbranded | unbranded | n/a | 0.9994 |
| Cutlery Set The Cake Story ⚠ | unbranded | branded | n/a | 0.7905 |
| Plastic Storage Container 500ml | unbranded | unbranded | n/a | 0.9989 |
| Korean LTO Menu | unbranded | unbranded | n/a | 0.9823 |
| Note Pad 3x3 | unbranded | unbranded | n/a | 0.9995 |
| Sumabrite Degreaser nd Heavy duty cleaner (break up HD) ⚠ | unbranded | branded | n/a | 0.9988 |
| Red Malka (Lal Masoor) Rajdhani ⚠ | unbranded | branded | n/a | 1.0000 |
| Silver Pouch 6*8 | unbranded | unbranded | n/a | 0.9999 |
| Triplesec ⚠ | unbranded | branded | n/a | 0.7663 |
| Shudh Garhwal - Khoya Pindi 1KG ⚠ | unbranded | branded | n/a | 0.9993 |
| #_# Chocolate Fudge Overload (NAS) 500 ml - Frozen Fun ⚠ | unbranded | branded | n/a | 0.9817 |
| Prepit Hyderabad Biriyan 1 kg ⚠ | unbranded | branded | n/a | 0.9996 |
| PLASTIC CONTAINER-150ML | unbranded | unbranded | n/a | 0.9984 |
| COLOUR CODE DOTT TUES ⚠ | unbranded | branded | n/a | 0.0331 |
| Red Chili Paste 1kg pkt | unbranded | unbranded | n/a | 0.9962 |
| Sweetpotato (Kanga) | unbranded | unbranded | n/a | 0.9996 |
| AANCH COVER ⚠ | unbranded | branded | n/a | 0.1689 |
| Dalchini | unbranded | unbranded | n/a | 0.9999 |
| Stone Flower(Dagad Phool) | unbranded | unbranded | n/a | 0.9999 |
| Sambal Oelek ⚠ | unbranded | branded | n/a | 0.1711 |
| Tandoori paneer tikka | unbranded | unbranded | n/a | 0.9984 |
| Cocoa powder (Medium Brown) Vanhouten ⚠ | unbranded | branded | n/a | 1.0000 |
| Brown Sugar Paste Fondant | unbranded | unbranded | n/a | 0.9997 |
| Butter Pouch 9X12 | unbranded | unbranded | n/a | 0.9997 |
| Good Night Machine ⚠ | unbranded | branded | n/a | 0.9756 |
| Biryani Handi 750 GM | unbranded | unbranded | n/a | 0.9598 |
| Green Tomato 1kg | unbranded | unbranded | n/a | 0.9998 |
| #_# Container lid - PMK Round Paper 500 ML Plastic - Prasuma ⚠ | unbranded | branded | n/a | 0.9649 |
| Envelope | unbranded | unbranded | n/a | 0.9991 |
| MF White Compound CO W33 ⚠ | unbranded | branded | n/a | 0.7372 |
| Kobij-Cabbage | unbranded | unbranded | n/a | 0.2975 |
| Garbage Bag Black 30 x50 | unbranded | unbranded | n/a | 0.9999 |
| #_# FC - Orange Popsicle Ice Cream [70 Ml] - Noto ⚠ | unbranded | branded | n/a | 0.9996 |
| Malas strawberry crush 750ml ⚠ | unbranded | branded | n/a | 0.9999 |
| Kit Kat ⚠ | unbranded | branded | n/a | 0.9998 |
| Perrier Water 330mL ⚠ | unbranded | branded | n/a | 0.9999 |
| DIGESTIVE BISCUITS | unbranded | unbranded | n/a | 0.9974 |
| SS Mould Round Cutter - 12pcs ⚠ | unbranded | branded | n/a | 0.0009 |
| TASKI R3 ⚠ | unbranded | branded | n/a | 0.9996 |
| Dollur Amla Jar ⚠ | unbranded | branded | n/a | 0.9689 |
| #_# Asafoetida / Hing - murukku | unbranded | unbranded | n/a | 0.9756 |
| 3 EASTMADE - BLACK PAPER WHOLE (KALI MIRCH) ⚠ | unbranded | branded | n/a | 0.9996 |
| Momo Steamer | unbranded | unbranded | n/a | 0.9972 |
| Dust Pan  Supli | unbranded | unbranded | n/a | 0.9864 |
| Potassium Sorbate | unbranded | unbranded | n/a | 0.9999 |
| Amla Sabut Herble | unbranded | unbranded | n/a | 0.9866 |
| Ro 48 ⚠ | unbranded | branded | n/a | 0.0260 |
| CUMIN WHOLE (JEERA) | unbranded | unbranded | n/a | 0.9993 |
| Green peas | unbranded | unbranded | n/a | 0.9994 |
| Maida Flour Premium (per kg) | unbranded | unbranded | n/a | 0.9698 |
| VKL PERI PERI MARINADE ⚠ | unbranded | branded | n/a | 0.9990 |
| Red Fondant | unbranded | unbranded | n/a | 0.9977 |
| Radish White | unbranded | unbranded | n/a | 0.9997 |
| SUMA TAB CHLORINE ⚠ | unbranded | branded | n/a | 0.9997 |
| PUMPKIN SEEDS (1Kg Pkt) | unbranded | unbranded | n/a | 0.9998 |
| GARBAGE COVER SMALL 17x19 - 51 MM | unbranded | unbranded | n/a | 0.9999 |
| Dhania Pudina Chutney-SNACC ⚠ | unbranded | branded | n/a | 0.9980 |
| MDH Chana Masala ⚠ | unbranded | branded | n/a | 1.0000 |
| Brown Onion | unbranded | unbranded | n/a | 1.0000 |
| Lettuce Patta | unbranded | unbranded | n/a | 0.9991 |
| #_# Caramelo Banditos Sticker - Cookie Cartel ⚠ | unbranded | branded | n/a | 0.7905 |
| Biryani small Box (Serve -1) | unbranded | unbranded | n/a | 0.9995 |
| Flexible Plastic Bags ( 5kg Small Size - Mithai & Namkeen) | unbranded | unbranded | n/a | 0.9997 |
| SS  NOODAL CHANNI ⚠ | unbranded | branded | n/a | 0.0004 |
| STICKER SHEEK KABAB ⚠ | unbranded | branded | n/a | 0.0041 |
| Sticker Veg 750 ml Container | unbranded | unbranded | n/a | 0.9433 |
| Cling Film | unbranded | unbranded | n/a | 0.9993 |
| Kale | unbranded | unbranded | n/a | 0.9961 |
| #_# BC - Aam Ice Cream [300ML] - BICO ⚠ | unbranded | branded | n/a | 0.9917 |
| 3 Ply Corrugated Croissant Tray | unbranded | unbranded | n/a | 0.9972 |
| Kundru | unbranded | unbranded | n/a | 0.9998 |
| Unbranded Spray Gun | unbranded | unbranded | n/a | 0.6225 |
| Sparkling Water | unbranded | unbranded | n/a | 0.9987 |
| Kung Pao Sauce 335 G ⚠ | unbranded | branded | n/a | 0.0357 |
| Plastic Packing Theli (PP) | unbranded | unbranded | n/a | 1.0000 |
| EVD DAIRY WHITENER 1 KG ⚠ | unbranded | branded | n/a | 0.9988 |
| #_# Big Blue Box - Sweetish ⚠ | unbranded | branded | n/a | 0.7249 |
| 19 KG Commercial Cylinder | unbranded | unbranded | n/a | 0.9800 |
| Message Card | unbranded | unbranded | n/a | 0.9828 |
| VIKRAM - CHAKKI ATTA 30 KG ⚠ | unbranded | branded | n/a | 0.9997 |
| Kashmiri Chili | unbranded | unbranded | n/a | 0.9989 |
| Texmex cheese sauce ⚠ | unbranded | branded | n/a | 0.0180 |
| Dried figs | unbranded | unbranded | n/a | 0.9972 |
| WOODEN SPOON 160MM (100 Pcs) | unbranded | unbranded | n/a | 0.9997 |
| UH ZUCCHINI GREENSMALL DICE1 KG / BAG | unbranded | unbranded | n/a | 0.9659 |
| #_# SIERRA 72% Dark Chocolate Bar - Ether ⚠ | unbranded | branded | n/a | 0.9820 |
| Butter Scotch DF Bite ⚠ | unbranded | branded | n/a | 0.9992 |
| GLOVES BLUE | unbranded | unbranded | n/a | 0.9999 |
| Milk Compound Slab M21 ⚠ | unbranded | branded | n/a | 0.4844 |
| Quinoa 1kg | unbranded | unbranded | n/a | 0.9966 |
| A-005 Grill and Oven Cleaner ACTON ⚠ | unbranded | branded | n/a | 0.9976 |
| Flow Wrap Rolls - Raspberry Duet (60 ml) ⚠ | unbranded | branded | n/a | 0.0316 |
| Garbage Bag 30x50 Kg | unbranded | unbranded | n/a | 0.9999 |
| Dry Amla-Dry Gooseberry | unbranded | unbranded | n/a | 0.9998 |
| Real Pineapple Juice ⚠ | unbranded | branded | n/a | 0.9990 |
| PG-Paper Tub Lids ⚠ | unbranded | branded | n/a | 0.4111 |
| Cambro Polycarbonate GN Pan 1/2 200mm ⚠ | unbranded | branded | n/a | 0.9999 |
| Mangoes (Sindhura) X1KG | unbranded | unbranded | n/a | 0.9999 |
| Premix Egg Free Chocolate Make: pillsbury ⚠ | unbranded | branded | n/a | 0.9999 |
| Masoor Whole | unbranded | unbranded | n/a | 0.9988 |
| Jau / Ghat | unbranded | unbranded | n/a | 0.9979 |
| Soda 750ml- @ 18% | unbranded | unbranded | n/a | 0.9857 |
| Blue Berry 250Gs | unbranded | unbranded | n/a | 0.9060 |
| Active X Mustard Oil 500mL ⚠ | unbranded | branded | n/a | 0.9998 |
| PRINTER ROLL | unbranded | unbranded | n/a | 0.9866 |
| #_# Frozen OG Chocolate Chip Chonker - Chonkers ⚠ | unbranded | branded | n/a | 0.9812 |
| Burata Cheese 250 Grm | unbranded | unbranded | n/a | 0.9774 |
| Mother Dairy milk ⚠ | unbranded | branded | n/a | 1.0000 |
| CELLO TAPE BIG PLAIN 3 INCH ⚠ | unbranded | branded | n/a | 0.7905 |
| Sweets Milk Kalakand | unbranded | unbranded | n/a | 0.9983 |
| #_# Greeting Card - Sassy Teaspoon ⚠ | unbranded | branded | n/a | 0.9504 |
| Kcco Tray Big ⚠ | unbranded | branded | n/a | 0.6406 |
| KESAR | unbranded | unbranded | n/a | 0.9185 |
| CARRY BAG 500GM | unbranded | unbranded | n/a | 0.9998 |
| #_# The Godfather (Reeses peanut butter cup) Cookie Dough - Cookie Cartel ⚠ | unbranded | branded | n/a | 0.9995 |
| DRY ICE | unbranded | unbranded | n/a | 0.9995 |
| #_# PMK Veg Hakka Noodles 250gm - Prasuma ⚠ | unbranded | branded | n/a | 0.9989 |
| Gud | unbranded | unbranded | n/a | 0.8500 |
| #_# French Vanilla (100 ml) - Go Zero ⚠ | unbranded | branded | n/a | 0.9990 |
| #_# Classic Vanilla Minis Sugar Free Ice cream [09 pieces] - Noto ⚠ | unbranded | branded | n/a | 0.9998 |
| PLASTIC DIP BOWL 50 ML | unbranded | unbranded | n/a | 0.9948 |
| SS GN PAN 1/3 100 MM ⚠ | unbranded | branded | n/a | 0.0001 |
| NATURESMITH PAPRIKA POWDER 60GM ⚠ | unbranded | branded | n/a | 1.0000 |
| FRENCH FRIES | unbranded | unbranded | n/a | 0.9957 |
| Poly Veg logo1500&#215;23 | unbranded | unbranded | n/a | 0.9918 |
| Hand Sanitizer | unbranded | unbranded | n/a | 0.9961 |
| Cutlery Basket | unbranded | unbranded | n/a | 0.9669 |
| PAPER CUP ( TEA WATER ETC) | unbranded | unbranded | n/a | 0.9996 |
| NOTEBOOK LONG 200 PAGES | unbranded | unbranded | n/a | 0.9999 |
| Rice Dosa (Ponni) | unbranded | unbranded | n/a | 0.9957 |
| #_# Kesar Peda 500gms - Genda Phool ⚠ | unbranded | branded | n/a | 0.9546 |
| XO Sauce Sticker ⚠ | unbranded | branded | n/a | 0.0015 |
| Dry Fruits Pista Whole | unbranded | unbranded | n/a | 0.9995 |
| Bru Coffee 500g ⚠ | unbranded | branded | n/a | 1.0000 |
| Hummus | unbranded | unbranded | n/a | 0.9898 |
| Lotus Flour ⚠ | unbranded | branded | n/a | 0.9610 |
| Nestle Milk Powder 1KG ⚠ | unbranded | branded | n/a | 1.0000 |
| UH GREEN CAPSICUMWHOLE CLEANEDCRATE | unbranded | unbranded | n/a | 0.9952 |
| Mustard Seed | unbranded | unbranded | n/a | 0.9848 |
| Roll Sleeve Red | unbranded | unbranded | n/a | 0.9990 |
| Cookies Caramel 6kg ( Mec3-14772) ⚠ | unbranded | branded | n/a | 0.9990 |
| River Sole Fillet | unbranded | unbranded | n/a | 0.9992 |
| HOLLO MAT3125*5 ⚠ | unbranded | branded | n/a | 0.5078 |
| Cotton BBK Apron ⚠ | unbranded | branded | n/a | 0.1711 |
| CC CONTAINER - 375ML | unbranded | unbranded | n/a | 0.9906 |
| Adrak / Ginger | unbranded | unbranded | n/a | 0.9996 |
| #_# Stapler | unbranded | unbranded | n/a | 0.9974 |
| Curry Patta | unbranded | unbranded | n/a | 0.9993 |
| Termocool morded box ⚠ | unbranded | branded | n/a | 0.8520 |
| #_# Cacao Crispy - Ether ⚠ | unbranded | branded | n/a | 0.4649 |
| Cake Saver ⚠ | unbranded | branded | n/a | 0.0003 |
| Milk ( Full Cream ) | unbranded | unbranded | n/a | 0.9984 |
| Dark Chocolate Paste-NAS ⚠ | unbranded | branded | n/a | 0.0351 |
| DAL MAKHANI STICKERS | unbranded | unbranded | n/a | 0.9928 |
| Mini Button Bhakarwadi | unbranded | unbranded | n/a | 0.9883 |
| Thai Jasmine Rice 2kg pkt MBK ⚠ | unbranded | branded | n/a | 0.9728 |
| Plastic Packing Cover Thick   12*16 | unbranded | unbranded | n/a | 1.0000 |
| Pesto Pistachio 2.5kg (Mec3-14755) ⚠ | unbranded | branded | n/a | 0.9997 |
| MAKKI ATTA | unbranded | unbranded | n/a | 0.9991 |
| Chest Freezer Capacity - 500 Ltr - 1060*700*840 | unbranded | unbranded | n/a | 0.9992 |
| Coke 750 Ml ⚠ | unbranded | branded | n/a | 1.0000 |
| Gherkin | unbranded | unbranded | n/a | 0.9948 |
| Palak - Spinach | unbranded | unbranded | n/a | 0.9997 |
| GLUTEN NB 0121 ⚠ | unbranded | branded | n/a | 0.8129 |
| 200m Tie | unbranded | unbranded | n/a | 0.7827 |
| SAMSEER MARK ⚠ | unbranded | branded | n/a | 0.2568 |
| Paper Cup 350ml (10'' Oz) FLYP ⚠ | unbranded | branded | n/a | 0.9826 |
| N_4  Pet Jar Lid | unbranded | unbranded | n/a | 0.9137 |
| Farali Sabudana Vada | unbranded | unbranded | n/a | 0.9989 |
| EGGFREE TEA TIME VANILLA MUFFIN ⚠ | unbranded | branded | n/a | 0.0685 |
| Noodle ( Thin Vala ) | unbranded | unbranded | n/a | 0.9972 |
| Hand Wash 5 Ltr Can | unbranded | unbranded | n/a | 0.9995 |
| Windmill Potato starch ⚠ | unbranded | branded | n/a | 0.9975 |
| CURRY PATTA | unbranded | unbranded | n/a | 0.9990 |
| #_# Mango Kulfi 300gm - Parsi Dairy Farm ⚠ | unbranded | branded | n/a | 1.0000 |
| Sweets Milk White Peda | unbranded | unbranded | n/a | 0.9992 |
| #_# Pista Kulfi Stick (70 ml) - Go Zero ⚠ | unbranded | branded | n/a | 0.9876 |
| Silver Pouch 6*8 (100PC) | unbranded | unbranded | n/a | 0.9999 |
| #_# Rocky Road Ice-cream Tub (100ml) - Meemees ⚠ | unbranded | branded | n/a | 0.9999 |
| Fruit Cocktail Tin ⚠ | unbranded | branded | n/a | 0.3998 |
| Hand Rub | unbranded | unbranded | n/a | 0.9993 |
| 500 ml rectangle box | unbranded | unbranded | n/a | 0.9998 |
| Chocolate Ice-cream | unbranded | unbranded | n/a | 0.9996 |
| WHITE PITA BREAD 4 PC PACK | unbranded | unbranded | n/a | 0.9995 |
| Turmeric (Haldi) Powder Chounk | unbranded | unbranded | n/a | 0.9756 |
| #_# Sugar Free Chocolate Hazelnut Ice Cream Tub (125 ml) - Bina ⚠ | unbranded | branded | n/a | 0.9987 |
| Dark Couverture 54% | unbranded | unbranded | n/a | 0.9990 |
| SCOTCH BRITE  JUNA ⚠ | unbranded | branded | n/a | 0.9972 |
| Thai Jasmine rice | unbranded | unbranded | n/a | 0.9974 |
| Biscoff Biscuit Lotus ⚠ | unbranded | branded | n/a | 1.0000 |
| CINNAMON 1 KG | unbranded | unbranded | n/a | 0.9998 |
| President Butter Unsalted 500gm ⚠ | unbranded | branded | n/a | 1.0000 |
| Milk | unbranded | unbranded | n/a | 0.9949 |
| Olive Oil (Regular /Pomace ) | unbranded | unbranded | n/a | 0.9989 |
| MRD Stickers ⚠ | unbranded | branded | n/a | 0.6370 |
| Milk Chocochip | unbranded | unbranded | n/a | 0.9965 |
| Urinal Pad | unbranded | unbranded | n/a | 0.9986 |
| Bombay pao | unbranded | unbranded | n/a | 0.9997 |
| Taski R5 5ltr ⚠ | unbranded | branded | n/a | 0.9999 |
| MANGO PUREE | unbranded | unbranded | n/a | 0.9993 |
| Magaj Big | unbranded | unbranded | n/a | 0.8933 |
| PAPER COVER BROWN - PAPAD | unbranded | unbranded | n/a | 0.9112 |
| Cake Box (7*7*4) | unbranded | unbranded | n/a | 1.0000 |
| Kabuli Channa | unbranded | unbranded | n/a | 0.9988 |
| Tahina Paste | unbranded | unbranded | n/a | 0.9928 |
| Sticker Mutton Haleem ⚠ | unbranded | branded | n/a | 0.0213 |
| Plastic Oven Bowl 2200 ml | unbranded | unbranded | n/a | 0.9985 |
| Raw Banana- Nos | unbranded | unbranded | n/a | 0.9998 |
| Disposal Cap (Pkt) | unbranded | unbranded | n/a | 0.9900 |
| InWard Register ⚠ | unbranded | branded | n/a | 0.0177 |
| Potato Flakes 1kg pkt | unbranded | unbranded | n/a | 0.9960 |
| DESERT SPOON 12GTIDY ⚠ | unbranded | branded | n/a | 0.0122 |
| Maggi Seasoning Sauce 680Ml ⚠ | unbranded | branded | n/a | 0.9999 |
| Pizza Base 8 inch Whole Wheat Pan Crust (Junos) ⚠ | unbranded | branded | n/a | 1.0000 |
| Topper ⚠ | unbranded | branded | n/a | 0.1176 |
| Staff Subji | unbranded | unbranded | n/a | 0.8723 |
| Brinjal   Black | unbranded | unbranded | n/a | 0.9998 |
| #_# Griselda's Red Velvet Sticker (Eggless) - Cookie Cartel ⚠ | unbranded | branded | n/a | 0.9196 |
| Canteen Tea Cup (130ML) | unbranded | unbranded | n/a | 0.9977 |
| CHICKEN LEG RAW | unbranded | unbranded | n/a | 0.9994 |
| #_# Sakura Blossom Gateaux (125 Gms) - Ether ⚠ | unbranded | branded | n/a | 0.9971 |
| TL Slicer Cutter ⚠ | unbranded | branded | n/a | 0.0981 |
| #_# XYLITOL Chocolate Hazelnut Icecream (600ML) - Bina ⚠ | unbranded | branded | n/a | 0.9504 |
| J and B Rare ⚠ | unbranded | branded | n/a | 0.9991 |
| Golden Dust ⚠ | unbranded | branded | n/a | 0.3141 |
| #_# Slide Tru Hamper Box OF 4 Outer - The Tiny Tub ⚠ | unbranded | branded | n/a | 0.9885 |
| Moth / Math Atta - Flour - Moth Beans | unbranded | unbranded | n/a | 0.9917 |
| Fork PLA 160 mm | unbranded | unbranded | n/a | 0.9997 |
| Hot Dog Bun 55g L 160mm X W 55mm | unbranded | unbranded | n/a | 0.9999 |
| Ajinomato ⚠ | unbranded | branded | n/a | 0.7154 |
| Cumin Seeds | unbranded | unbranded | n/a | 0.9951 |
| PAPAYA | unbranded | unbranded | n/a | 0.9996 |
| Bed Sheet | unbranded | unbranded | n/a | 0.9736 |
| Twinings strawberry green tea ⚠ | unbranded | branded | n/a | 1.0000 |
| CHICKEN KEEMA FOR SEEKH | unbranded | unbranded | n/a | 0.9985 |
| Fryola Oil ⚠ | unbranded | branded | n/a | 0.9994 |
| Madhusudan Butter ⚠ | unbranded | branded | n/a | 1.0000 |
| Gulab Jamun (Wyn) ⚠ | unbranded | branded | n/a | 0.9974 |
| Sweets Pcs. Rasmalai | unbranded | unbranded | n/a | 0.9997 |
| #_# Soaked Chia - The Whole Truth ⚠ | unbranded | branded | n/a | 0.9967 |
| Soda Water Kinley 750 ml ⚠ | unbranded | branded | n/a | 1.0000 |
| #_# Tango Mango - Anando ⚠ | unbranded | branded | n/a | 0.8634 |
| Fresh Milk (Full Cream) | unbranded | unbranded | n/a | 0.9903 |
| Food Colours Splash 200g Assorted ⚠ | unbranded | branded | n/a | 0.3702 |
| Milkhana Melted Cheese ⚠ | unbranded | branded | n/a | 0.9900 |
| #_# Sticker - Sauce Dip Sticker Crunchy Chilli Oil - Prasuma ⚠ | unbranded | branded | n/a | 0.9881 |
| POTATO STARCH | unbranded | unbranded | n/a | 0.9997 |
| MAPRO BLACK CURRANT 1 LTR ⚠ | unbranded | branded | n/a | 1.0000 |
| CELLOFIN PAPER ⚠ | unbranded | branded | n/a | 0.7578 |
| Paper Cup Holder | unbranded | unbranded | n/a | 0.9997 |
| BARDINET BRANDY 1000 ML ⚠ | unbranded | branded | n/a | 0.0326 |
| #_# Tender Coconut Litchi Ice Pop - Getaway ⚠ | unbranded | branded | n/a | 0.9910 |
| Number Candles | unbranded | unbranded | n/a | 0.9979 |
| Papaya | unbranded | unbranded | n/a | 0.9997 |
| Mixed Veg Pickle (5 kg)-Snacc ⚠ | unbranded | branded | n/a | 0.9995 |
| Cooking White Wine 750ml | unbranded | unbranded | n/a | 0.9995 |
| SPINCACH | unbranded | unbranded | n/a | 0.9874 |
| Cake Base 5.5x5.5 Plain | unbranded | unbranded | n/a | 0.9997 |
| Yellow Moong dal | unbranded | unbranded | n/a | 0.9994 |
| PAPER COVER BROWN -S - CHUTNEY | unbranded | unbranded | n/a | 0.9966 |
| #_# Mango Biscoff Tub - Sassy Teaspoon ⚠ | unbranded | branded | n/a | 0.9996 |
| KALI MASOOR | unbranded | unbranded | n/a | 0.9859 |
| #_# Plain Milk Chocolate Bar 41% [65 g] - Entisi Chocolatier ⚠ | unbranded | branded | n/a | 1.0000 |
| SCOTCH BRITE - SOFT SPONGE ⚠ | unbranded | branded | n/a | 0.9996 |
| Vinyl Sticker 2x1.5 Ft | unbranded | unbranded | n/a | 0.9999 |
| Veggie Pizza Pocket | unbranded | unbranded | n/a | 0.9985 |
| Soyabeen Chunks-Soya Chunks | unbranded | unbranded | n/a | 0.9958 |
| #_# Sugar Free Coffee Almond Ice Cream Tub (125 ml) - Bina ⚠ | unbranded | branded | n/a | 0.9968 |
| COOK POT SS WITH LID 36*20  20LTR | unbranded | unbranded | n/a | 0.9995 |
| PERFECT NO-BAKE CHEESECAKE MIX (1KG) ⚠ | unbranded | branded | n/a | 0.8539 |
| HAMDARD ROOHAFZA 750ML ⚠ | unbranded | branded | n/a | 1.0000 |
| Chef Coat S36  Black Half Sleeve ⚠ | unbranded | branded | n/a | 0.0357 |
| Fruit Filling Mango Delta ⚠ | unbranded | branded | n/a | 0.8056 |
| Chocolate Sprinkle | unbranded | unbranded | n/a | 0.9971 |
| 250ML Tea Pouch with Box | unbranded | unbranded | n/a | 0.9995 |
| Fresh Cream - 250ml | unbranded | unbranded | n/a | 0.9972 |
| Aroma Diffuser Liquid | unbranded | unbranded | n/a | 0.9976 |
| Hot dog 7 inch with seeds | unbranded | unbranded | n/a | 0.9990 |
| WF - 350 ml Bowl | unbranded | unbranded | n/a | 0.9969 |
| #_# Blueberry Greek Yogurt Minis Guilt Free Ice Cream [09 pieces] - Noto ⚠ | unbranded | branded | n/a | 0.9998 |
| Lychee Juice 1000 Ml | unbranded | unbranded | n/a | 0.9988 |
| #_# The Berry Good Bar 72% [Chocolate Bar] - La Folie ⚠ | unbranded | branded | n/a | 0.9997 |
| 12OZ CLEAR PET CUPS | unbranded | unbranded | n/a | 0.9999 |
| Brioche Buns 70g D 100mm X H 45mm | unbranded | unbranded | n/a | 0.9999 |
| #_# Mustard Seeds Temper/Tadka - Murukku | unbranded | unbranded | n/a | 0.3416 |
| Jeera Whole Grade 1 | unbranded | unbranded | n/a | 0.9974 |
| Goodlife Milk 1ltr pkt Nandini ⚠ | unbranded | branded | n/a | 1.0000 |
| Unbranded Wooden Spoon- 100pcs | unbranded | unbranded | n/a | 0.9924 |
| Fortune Aata ⚠ | unbranded | branded | n/a | 0.9998 |
| Sargvo-Drumsticks | unbranded | unbranded | n/a | 0.9497 |
| preethi xpro Duo mg-198 1300w ⚠ | unbranded | branded | n/a | 1.0000 |
| Chonak | unbranded | unbranded | n/a | 0.9990 |
| Corn Flour Weikfield ⚠ | unbranded | branded | n/a | 1.0000 |
| Tea Powder   Red Label 1kg pkt ⚠ | unbranded | branded | n/a | 1.0000 |
| CHUNDAKKAI VATHAL | unbranded | unbranded | n/a | 0.9999 |
| Fees for plumber | unbranded | unbranded | n/a | 0.9965 |
| Sharpner | unbranded | unbranded | n/a | 0.9973 |
| Plastic Ch. Mat | unbranded | unbranded | n/a | 0.9442 |
| Oat Milk AltCo. 200 ml ⚠ | unbranded | branded | n/a | 0.9999 |
| Sauce-Schezwan | unbranded | unbranded | n/a | 0.9984 |
| Tapioca Starch 500g pkt | unbranded | unbranded | n/a | 0.9995 |
| Cremica Chef Choice Mayo ⚠ | unbranded | branded | n/a | 1.0000 |
| #_# Box of 20 Assorted Ganaches - La Folie ⚠ | unbranded | branded | n/a | 0.9992 |
| Red Cherry with Stem 850g Tin | unbranded | unbranded | n/a | 0.9934 |
| Black Container 1000 ml with partition Lid | unbranded | unbranded | n/a | 0.9998 |
| Cheddar White Wyke 2.5 Kg ⚠ | unbranded | branded | n/a | 0.9999 |
| Boba Lychee can ⚠ | unbranded | branded | n/a | 0.0001 |
| Stainless Steel Scrub | unbranded | unbranded | n/a | 0.9996 |
| Coconut milk powder maggi ⚠ | unbranded | branded | n/a | 0.9702 |
| Malas Orange Crush 750ml ⚠ | unbranded | branded | n/a | 0.9999 |
| Citric Acid Monohydrate 500 GM | unbranded | unbranded | n/a | 0.9996 |
| Ajinomoto (Golden Crown) ⚠ | unbranded | branded | n/a | 0.9977 |
| Chocolate Hamper 812 ⚠ | unbranded | branded | n/a | 0.2121 |
| #_# Hamper Box Of 2 Outer  - The Tiny Tub ⚠ | unbranded | branded | n/a | 0.7853 |
| Hoegaarden Belgian Blanche ⚠ | unbranded | branded | n/a | 1.0000 |
| #_# Double Cocoa Protien Bar - The Whole Truth ⚠ | unbranded | branded | n/a | 0.9998 |
| Cinnamon Stick Dalchini | unbranded | unbranded | n/a | 0.9995 |
| DUSTER YELLOW | unbranded | unbranded | n/a | 0.9831 |
| #_# Guava Pop (70 ML) - Noto ⚠ | unbranded | branded | n/a | 0.9983 |
| Chicken Broth Powder Knorr ⚠ | unbranded | branded | n/a | 1.0000 |
| Sprite 300 ml ⚠ | unbranded | branded | n/a | 1.0000 |
| Papaya Green | unbranded | unbranded | n/a | 0.9872 |
| Tata Agni Dust Tea 1 kg ⚠ | unbranded | branded | n/a | 1.0000 |
| Plastic Container (Round) - 250 ml | unbranded | unbranded | n/a | 0.9998 |
| Urad Wash | unbranded | unbranded | n/a | 0.9466 |
| Cmc Powder ⚠ | unbranded | branded | n/a | 0.0005 |
| Cashewnut -2 pcs | unbranded | unbranded | n/a | 0.9992 |
| Tom Kha Paste 1kg pkt ⚠ | unbranded | branded | n/a | 0.0706 |
| #_# Double Chocolate Chip Cookie Premix - 8 pcs - Sweetish ⚠ | unbranded | branded | n/a | 0.9674 |
| Mango Juice 1000 Ml | unbranded | unbranded | n/a | 0.9974 |
| SOUR DOUGH BREAD | unbranded | unbranded | n/a | 0.9999 |
| 95 Die lid | unbranded | unbranded | n/a | 0.8500 |
| CHAT PLATE 6 INCH | unbranded | unbranded | n/a | 0.9992 |
| Frozen Sea Bass Fillets | unbranded | unbranded | n/a | 0.9990 |
| Amul Cheese Spread 200 Gm ⚠ | unbranded | branded | n/a | 1.0000 |
| Rice Flat Noodle 10mm   500g pkt   How How ⚠ | unbranded | branded | n/a | 0.9999 |
| Yellow Color | unbranded | unbranded | n/a | 0.6893 |
| DISPOSIBLE GLOVES | unbranded | unbranded | n/a | 0.9966 |
| Pillar | unbranded | unbranded | n/a | 0.8634 |
| MOONG DHULI DAL | unbranded | unbranded | n/a | 0.9990 |
| A4 SIZE PAPER | unbranded | unbranded | n/a | 0.9990 |
| Floor Broom- Kharata | unbranded | unbranded | n/a | 0.9993 |
| Tomato ( For Gravy ) | unbranded | unbranded | n/a | 0.9990 |
| Party Popper 40 CM | unbranded | unbranded | n/a | 0.9996 |
| Coffee essence | unbranded | unbranded | n/a | 0.9929 |
| Dosa Batter Chilled | unbranded | unbranded | n/a | 0.9989 |
| Floor Cleaner 5 Ltr | unbranded | unbranded | n/a | 0.9997 |
| Wonder Wipes ⚠ | unbranded | branded | n/a | 0.9976 |
| Butter Paper - Cassata (r=73mm) | unbranded | unbranded | n/a | 0.9979 |
| Black Fungus | unbranded | unbranded | n/a | 0.9993 |
| Unbranded Black Pepper Whole 250gm | unbranded | unbranded | n/a | 0.9991 |
| Cashew Half | unbranded | unbranded | n/a | 0.9939 |
| Valencia Orange | unbranded | unbranded | n/a | 0.9998 |
| kikkoman Soya Sauce ⚠ | unbranded | branded | n/a | 1.0000 |
| MILK | unbranded | unbranded | n/a | 0.9984 |
| Truffle Paste (500gm Pack) ⚠ | unbranded | branded | n/a | 0.0001 |
| Elastic thread round black 1.1 MM | unbranded | unbranded | n/a | 0.9999 |
| Javitri (Mace) | unbranded | unbranded | n/a | 0.9985 |
| Date Label Sticker | unbranded | unbranded | n/a | 0.9914 |
| Gas Lighter | unbranded | unbranded | n/a | 0.9987 |
| #_# Hazelnut Mousse Cake [500 gms] [Gluten Free] - Sassy Teaspoon ⚠ | unbranded | branded | n/a | 0.9992 |
| Duster | unbranded | unbranded | n/a | 0.9716 |
| Rose Loose | unbranded | unbranded | n/a | 0.9977 |
| GTC Pizza Box 9x9 ⚠ | unbranded | branded | n/a | 0.9679 |
| CHICKEN THIGH BONELESS (80 - 90 gm) | unbranded | unbranded | n/a | 1.0000 |
| RED LABEL TEA (1 KG) ⚠ | unbranded | branded | n/a | 1.0000 |
| Biryani Box Printed Round with Lid (1250 gm) | unbranded | unbranded | n/a | 0.9707 |
| Thai Chilli Paste | unbranded | unbranded | n/a | 0.9998 |
| Almond Croissant Sticker (TH) | unbranded | unbranded | n/a | 0.9982 |
| BASMATI BIRYANI RICE | unbranded | unbranded | n/a | 0.9997 |
| Orange/Malta | unbranded | unbranded | n/a | 0.9977 |
| Oyester Sauce- non veg | unbranded | unbranded | n/a | 0.9942 |
| Coconut Water | unbranded | unbranded | n/a | 0.9992 |
| Nihari Masala  (Shan) ⚠ | unbranded | branded | n/a | 1.0000 |
| Pili mirch powder / yellow chilli powder | unbranded | unbranded | n/a | 0.9993 |
| Nihari Masala | unbranded | unbranded | n/a | 0.9870 |
| Cantener Half | unbranded | unbranded | n/a | 0.8741 |
| Chicken PCP (Bone) | unbranded | unbranded | n/a | 0.9901 |
| Cotton Dusters 21cm X 21cm | unbranded | unbranded | n/a | 0.9999 |
| Wrapper Yellow (12x12) for FLYP | unbranded | unbranded | n/a | 0.9124 |
| Wonder Wipe (3pc) ⚠ | unbranded | branded | n/a | 0.9803 |
| Nam Shop Sticker   Prawn Crackers Large ⚠ | unbranded | branded | n/a | 0.4805 |
| SS GN PAN LID 1/6 | unbranded | unbranded | n/a | 0.9999 |
| IDLY POWDER | unbranded | unbranded | n/a | 0.9963 |
| RASPBERRY IQF FROZEN | unbranded | unbranded | n/a | 0.9995 |
| Ciclo Printed Cake Box 2Pc ⚠ | unbranded | branded | n/a | 0.8176 |
| Plastic Film Pouch 7*10 80 Mic | unbranded | unbranded | n/a | 0.9999 |
| JK Copier A4 Paper ⚠ | unbranded | branded | n/a | 0.9999 |
| Tea flask - 250 ML -Outer coorugated Box-Snacc ⚠ | unbranded | branded | n/a | 0.8903 |
| Tikona Paratha | unbranded | unbranded | n/a | 0.9770 |
| Blue Pine Artesian Water - 750 ML - GST @18 % ⚠ | unbranded | branded | n/a | 0.9992 |
| Green Peas | unbranded | unbranded | n/a | 0.9965 |
| Non Veg Spring Rolls -SNACC ⚠ | unbranded | branded | n/a | 0.9937 |
| MUTTON BRAIN 1PCS | unbranded | unbranded | n/a | 0.9989 |
| Mapro Strawberry  Berry Crush-5 Ltr ⚠ | unbranded | branded | n/a | 1.0000 |
| ALUMINIUM CONTAINER LID 750ML | unbranded | unbranded | n/a | 0.9998 |
| Sauce Chilli Green Tops ⚠ | unbranded | branded | n/a | 0.9912 |
| SOYA CHAAP STUFFED SF | unbranded | unbranded | n/a | 0.9841 |
| Dry Ice | unbranded | unbranded | n/a | 0.9995 |
| Sugar (Chini) | unbranded | unbranded | n/a | 0.9993 |
| Gold Bark (Leaf) | unbranded | unbranded | n/a | 0.9546 |
| Amrut fusion single malt whisky 750 ml ⚠ | unbranded | branded | n/a | 0.9999 |
| TL Hitachi UX Makeup 800ml ⚠ | unbranded | branded | n/a | 0.1624 |
| TG-Party Snacks 35G Pouch ⚠ | unbranded | branded | n/a | 0.9732 |
| Monin Peach flavour ⚠ | unbranded | branded | n/a | 0.9999 |
| GARBAGE BAG GREEN | unbranded | unbranded | n/a | 0.9999 |
| GREEN CHILLI | unbranded | unbranded | n/a | 0.9999 |
| PAPER NAPKIN - 12CM X12 CM - PLAIN - LOCAL - PKT | unbranded | unbranded | n/a | 0.9994 |
| Note Book 240 Pages | unbranded | unbranded | n/a | 0.9996 |
| GFB Mushroom Patty ⚠ | unbranded | branded | n/a | 0.9971 |
| ATTA GANGA ⚠ | unbranded | branded | n/a | 0.9853 |
| MINERAL WATER BOTTLE 1 LIT SF ⚠ | unbranded | branded | n/a | 0.1128 |
| KAFFIR LIME | unbranded | unbranded | n/a | 0.9988 |
| #_# COCO 40% Dark Chocolate - Ether ⚠ | unbranded | branded | n/a | 0.9914 |
| White Pepper MDH 100 Gms ⚠ | unbranded | branded | n/a | 1.0000 |
| #_# Lotus Biscoff Icecream (125ML) - Bina ⚠ | unbranded | branded | n/a | 0.9997 |
| Water Chestnut In Water 567G | unbranded | unbranded | n/a | 0.9935 |
| ROSE MARY ⚠ | unbranded | branded | n/a | 0.2309 |
| #_# Baked Oregano Cheese Matthi - Genda Phool ⚠ | unbranded | branded | n/a | 0.8199 |
| STICKER SALAD ⚠ | unbranded | branded | n/a | 0.2509 |
| Kesari Color | unbranded | unbranded | n/a | 0.9702 |
| 1200 ML ROUND CONTAINER | unbranded | unbranded | n/a | 0.9985 |
| Lemon Grass (Green) | unbranded | unbranded | n/a | 0.9998 |
| SOYABEEN RAW | unbranded | unbranded | n/a | 0.9998 |
| #_# Mysore Chutney Frozen - Murukku | unbranded | unbranded | n/a | 0.8741 |
| Vanaspati 1kg pkt ⚠ | unbranded | branded | n/a | 0.2539 |
| Green Grapes | unbranded | unbranded | n/a | 0.9998 |
| Bayleaf Chounk | unbranded | unbranded | n/a | 0.9707 |
| Breakfast Sugar Trust 1 Kg ⚠ | unbranded | branded | n/a | 0.9724 |
| JALI MAT 10MM HEAVY | unbranded | unbranded | n/a | 0.9945 |
| Breakfast Sugar 1Kg | unbranded | unbranded | n/a | 0.9843 |
| Paper Straws 6mm (100PC) | unbranded | unbranded | n/a | 0.9994 |
| Liquid Glucose | unbranded | unbranded | n/a | 0.9997 |
| GARLIC WHOLE | unbranded | unbranded | n/a | 0.9997 |
| RAJDHANI - SOOJI (1KG) ⚠ | unbranded | branded | n/a | 1.0000 |
| Mutton currycut | unbranded | unbranded | n/a | 0.9989 |
| Thermal Paper Roll   Billing | unbranded | unbranded | n/a | 0.9994 |
| SP Thundercrush French Fries 9mm ⚠ | unbranded | branded | n/a | 0.9540 |
| Milk Powder Nestle 1 Kg ⚠ | unbranded | branded | n/a | 1.0000 |
| RAMPURI MIRCH | unbranded | unbranded | n/a | 0.9977 |
| PAPER NAPKINS | unbranded | unbranded | n/a | 0.9993 |
| Vat 69 ⚠ | unbranded | branded | n/a | 0.9999 |
| Cavity for corrugated box 720ml | unbranded | unbranded | n/a | 0.9997 |
| Aampanna juice 150ml ⚠ | unbranded | branded | n/a | 0.0014 |
| Cambro Polycarbonate LID for GN Pan 1/1 ⚠ | unbranded | branded | n/a | 0.9991 |
| Toned Tetra Milk 1000 ml | unbranded | unbranded | n/a | 0.9987 |
| Macroni Rajdhani ⚠ | unbranded | branded | n/a | 0.9998 |
| Grover Selecte Chenin Blanc 750 Ml ⚠ | unbranded | branded | n/a | 0.9992 |
| Oaksmith ⚠ | unbranded | branded | n/a | 0.9949 |
| Zukni Green ⚠ | unbranded | branded | n/a | 0.1259 |
| Packing tray ( 60x60x25mm ) | unbranded | unbranded | n/a | 0.9992 |
| Tandoori Chicken Masala Powder | unbranded | unbranded | n/a | 0.9974 |
| Paper Napkin Tissue 16x16 2ply | unbranded | unbranded | n/a | 1.0000 |
| #_# Cothas Blend Coffee 200 Gm - Murukku ⚠ | unbranded | branded | n/a | 0.2309 |
| Icing Sugar Powder | unbranded | unbranded | n/a | 0.9978 |
| Kumatia | unbranded | unbranded | n/a | 0.6225 |
| #_# Stirrer - Murukku | unbranded | unbranded | n/a | 0.7905 |
| #_# Assorted Roleys (Box of 6) - Meemees ⚠ | unbranded | branded | n/a | 0.9790 |
| White Peas Batani | unbranded | unbranded | n/a | 0.9997 |
| Diya Oil | unbranded | unbranded | n/a | 0.9621 |
| #_# Cassata (110 ml) - Go Zero ⚠ | unbranded | branded | n/a | 0.9951 |
| Farali Chevdo (Tikho) | unbranded | unbranded | n/a | 0.8977 |
| Manager Shirt Pink Size-S | unbranded | unbranded | n/a | 0.9800 |
| Aluminium Container 750ml with Lid (Outlet) | unbranded | unbranded | n/a | 0.9993 |
| Coconut Dry whole | unbranded | unbranded | n/a | 0.9998 |
| Meat Masala MDH ⚠ | unbranded | branded | n/a | 1.0000 |
| #_# Black Ceaser Dough - Cookie Cartel ⚠ | unbranded | branded | n/a | 0.9831 |
| AA seal stickers | unbranded | unbranded | n/a | 0.9981 |
| Chavali Red | unbranded | unbranded | n/a | 0.9977 |
| Dabur Honey ⚠ | unbranded | branded | n/a | 0.9997 |
| #_# Baguette Sourdough - La folie ⚠ | unbranded | branded | n/a | 0.9935 |
| #_# Tag - Gluten-free Paleo Cookies - Le Four ⚠ | unbranded | branded | n/a | 0.9965 |
| #_# The Great Indian Toffee 300gm - Parsi Dairy Farm ⚠ | unbranded | branded | n/a | 0.9997 |
| Fanta Can 300ml-GST@ 28% ⚠ | unbranded | branded | n/a | 1.0000 |
| Fevicol 1 Kg ⚠ | unbranded | branded | n/a | 0.9997 |
| Panner Fresh 1 kg | unbranded | unbranded | n/a | 0.7905 |
| Saffron Kessar | unbranded | unbranded | n/a | 0.9019 |
| HING (LG) ⚠ | unbranded | branded | n/a | 0.0888 |
| Lid for paperbowl 500ml | unbranded | unbranded | n/a | 0.9997 |
| Dustbin Cover Small | unbranded | unbranded | n/a | 0.9979 |
| MUMBAI RAVA 5 KG ⚠ | unbranded | branded | n/a | 0.1097 |
| Gochujang 17kg Tin ⚠ | unbranded | branded | n/a | 0.7058 |
| Garbage Bag Green 30 X50 | unbranded | unbranded | n/a | 1.0000 |
| Timmys Food Bag ⚠ | unbranded | branded | n/a | 0.6619 |
| Palm Jaggery (per kg) | unbranded | unbranded | n/a | 0.9998 |
| Duster Check/Hand | unbranded | unbranded | n/a | 0.9196 |
| CARNATTION MILK  405 GM ( EVAPORATED MILK ) ⚠ | unbranded | branded | n/a | 1.0000 |
| 11.5x11.5 (Round) Sandhouse Butter paper (40GSM) ⚠ | unbranded | branded | n/a | 0.8397 |
| Micks Lotus Biscoff Biscuit ⚠ | unbranded | branded | n/a | 0.9999 |
| SDU Deva Chardonnay White wine 750ml ⚠ | unbranded | branded | n/a | 0.9993 |
| Quinoa 1 kg | unbranded | unbranded | n/a | 0.9980 |
| Amul Fresh Cream 1 Ltr- Exempt ⚠ | unbranded | branded | n/a | 0.9999 |
| Duster cloth-Thick Mop | unbranded | unbranded | n/a | 0.9970 |
| Hand Sanitizer HS 100 ⚠ | unbranded | branded | n/a | 0.2227 |
| Palak paste | unbranded | unbranded | n/a | 0.9955 |
| Squeeze bottles -  Large | unbranded | unbranded | n/a | 0.9987 |
| VINEGAR SYNTHETIC 750ML | unbranded | unbranded | n/a | 0.9998 |
| Salt Black Tiger | unbranded | unbranded | n/a | 0.1277 |
| Bread Crumb (Orange) | unbranded | unbranded | n/a | 0.9986 |
| Chicken Lollypop Plate | unbranded | unbranded | n/a | 0.9992 |
| FRENCH HEARTS VINYL STICKER SET ⚠ | unbranded | branded | n/a | 0.0000 |
| Gram Flour/Besan (Motichur) | unbranded | unbranded | n/a | 0.9906 |
| Chicken Galouti | unbranded | unbranded | n/a | 0.9996 |
| Garbage Bags 29*39 | unbranded | unbranded | n/a | 0.9998 |
| Slider Bun 25GMS x 3'' | unbranded | unbranded | n/a | 0.9997 |
| BLACK PAPER | unbranded | unbranded | n/a | 0.0001 |
| #_# Baked Salted Caramel Cheesecake - Sassy Teaspoon ⚠ | unbranded | branded | n/a | 0.9996 |
| McCain Rosti Round/ Hash Brown 1.5kg ⚠ | unbranded | branded | n/a | 1.0000 |
| Sriracha (570gm bottle) ⚠ | unbranded | branded | n/a | 0.9474 |
| #_# Gate Pass Book ⚠ | unbranded | branded | n/a | 0.0012 |
| CHANA MASALA MDH 100GM ⚠ | unbranded | branded | n/a | 1.0000 |
| Knor Aromat Seasoning ⚠ | unbranded | branded | n/a | 0.9979 |
| Tape Dispenser | unbranded | unbranded | n/a | 0.9740 |
| Agnessi Penne Pasta ⚠ | unbranded | branded | n/a | 1.0000 |
| Pet Jar 6 inch | unbranded | unbranded | n/a | 0.9972 |
| Rasila Rajma - Outsource | unbranded | unbranded | n/a | 0.9315 |
| Maida DFM 50 Kg Unbrand | unbranded | unbranded | n/a | 0.9990 |
| Budweiser Premium ⚠ | unbranded | branded | n/a | 0.9684 |
| Kissan Tomato Sause Dip ⚠ | unbranded | branded | n/a | 0.9996 |
| RAGI WHOLE | unbranded | unbranded | n/a | 0.9992 |
| Cotton pink plan shirt  (Size-XXL) | unbranded | unbranded | n/a | 0.9992 |
| Coffee powder Nescafe 500 gm ⚠ | unbranded | branded | n/a | 1.0000 |
| TOP COVER OF BOX 750 ML SALADSPOINT ⚠ | unbranded | branded | n/a | 0.9185 |
| FULL CREAM MILK | unbranded | unbranded | n/a | 0.9983 |
| Diversey Spray Bottles ⚠ | unbranded | branded | n/a | 0.9980 |
| Kakdi - Cucumber | unbranded | unbranded | n/a | 0.9998 |
| English Toffee | unbranded | unbranded | n/a | 0.9990 |
| BIRTHDAY CAP BOY | unbranded | unbranded | n/a | 0.9974 |
| #_# Roasted Chana Dal - Murukku | unbranded | unbranded | n/a | 0.9149 |
| Taski D9 (5lt) ⚠ | unbranded | branded | n/a | 0.9998 |
| Truffle Oil Urbani 250 ml ⚠ | unbranded | branded | n/a | 1.0000 |
| Kaffir Lime Leaves | unbranded | unbranded | n/a | 0.9999 |
| Aniseed Whole - Saunf | unbranded | unbranded | n/a | 0.9935 |
| Chocolate Hamper 1864 ⚠ | unbranded | branded | n/a | 0.0434 |
| Flax Seeds Plain | unbranded | unbranded | n/a | 0.9986 |
| #_# Wooden Spoon - Amore ⚠ | unbranded | branded | n/a | 0.7773 |
| Chili Powder 1kg pkt | unbranded | unbranded | n/a | 0.9997 |
| Strawberry | unbranded | unbranded | n/a | 0.9995 |
| Maida Kesari Brand 50kgs ⚠ | unbranded | branded | n/a | 0.9946 |
| Gherkin (pickled Cucumber whole) | unbranded | unbranded | n/a | 0.9933 |
| Brown Sugar sachet | unbranded | unbranded | n/a | 0.9994 |
| Jackfruit Cut (kathal) | unbranded | unbranded | n/a | 0.9999 |
| Kasoori Methi Dry 100GM | unbranded | unbranded | n/a | 0.9855 |
| HONEY GOCHUJANG SAUCE | unbranded | unbranded | n/a | 0.9982 |
| Non woven bag cinnamon big | unbranded | unbranded | n/a | 0.9974 |
| Ashok Besan ⚠ | unbranded | branded | n/a | 1.0000 |
| AJINO MOTO ⚠ | unbranded | branded | n/a | 0.9998 |
| SEED TIL WHITE NYLON | unbranded | unbranded | n/a | 0.1082 |
| CHILLY POWDER  1KG | unbranded | unbranded | n/a | 0.9992 |
| #_# Kulfi Insulation Bag - Parsi Dairy Farm ⚠ | unbranded | branded | n/a | 0.9988 |
| Natural Mineral Water Aava 500 ml ⚠ | unbranded | branded | n/a | 1.0000 |
| Parmesan Cheese 1kg | unbranded | unbranded | n/a | 0.9967 |
| Plain Container - Classic Cassata (110 ml) ⚠ | unbranded | branded | n/a | 0.5000 |
| Colin Spray 500ml ⚠ | unbranded | branded | n/a | 1.0000 |
| Pink Gel Colour | unbranded | unbranded | n/a | 0.9994 |
| Stamp Pad Medium Blue | unbranded | unbranded | n/a | 0.9994 |
| Frozen Beans (1Kg) | unbranded | unbranded | n/a | 0.9987 |
| Kaju 4pcs | unbranded | unbranded | n/a | 0.9994 |
| BROWN BUN | unbranded | unbranded | n/a | 0.9993 |
| #_# Jar - Death By Chocolate - Getaway ⚠ | unbranded | branded | n/a | 0.2200 |
| #_# Motichur Laddu 500gms - Dadus ⚠ | unbranded | branded | n/a | 0.9997 |
| #_# Mop Refill [Wet] | unbranded | unbranded | n/a | 0.9482 |
| Turmeric Powder 500 grams | unbranded | unbranded | n/a | 0.9985 |
| #_# Caramelo Banditos Dough - Cookie Cartel ⚠ | unbranded | branded | n/a | 0.9972 |
| Cheese Slice 200nos X 11.35g 2.27 Kg | unbranded | unbranded | n/a | 0.9968 |
| SS Round Plate 10 Inch- Order Plate | unbranded | unbranded | n/a | 0.9958 |
| Milk Premium Farm Fresh 1 Ltr | unbranded | unbranded | n/a | 0.9711 |
| Pitambari 150 gm ⚠ | unbranded | branded | n/a | 0.9974 |
| Raspberry Fruit | unbranded | unbranded | n/a | 0.9997 |
| GREEN CURRY PASTE NAMJAI 1 KG ⚠ | unbranded | branded | n/a | 1.0000 |
| #_# Scissor | unbranded | unbranded | n/a | 0.8311 |
| AMUL CHEESE SP PLAIN ⚠ | unbranded | branded | n/a | 1.0000 |
| 2 Cp-Snacc ⚠ | unbranded | branded | n/a | 0.1824 |
| #_# Sweet Chilli Sauce 15g - Prasuma ⚠ | unbranded | branded | n/a | 0.9996 |
| Transfer Notebook | unbranded | unbranded | n/a | 0.9976 |
| Korean Chilli Powder 300 gm | unbranded | unbranded | n/a | 0.9985 |
| 110 Ml Tea paper cup-Snacc ⚠ | unbranded | branded | n/a | 0.8199 |
| Fajita Topping | unbranded | unbranded | n/a | 0.9961 |
| Plastic Storage Boxes - Meduim | unbranded | unbranded | n/a | 0.9947 |
| Sugar Regular | unbranded | unbranded | n/a | 0.9961 |
| SHIKANJI MASALA | unbranded | unbranded | n/a | 0.9965 |
| Crunchy butterscotch PP 100ML | unbranded | unbranded | n/a | 0.9458 |
| Nestle Water (19 Litre) ⚠ | unbranded | branded | n/a | 1.0000 |
| ALMOND(BADAM) | unbranded | unbranded | n/a | 0.9997 |
| QT Rail ⚠ | unbranded | branded | n/a | 0.9659 |
| SUGAR | unbranded | unbranded | n/a | 0.9989 |
| Kitchen King MDH 100 Gm- GST @ 5% ⚠ | unbranded | branded | n/a | 0.9999 |
| CHAPAD HEAVY | unbranded | unbranded | n/a | 0.9711 |
| MANGO JUICE 1 LTR ⚠ | unbranded | branded | n/a | 0.8903 |
| Lettuce Lollo Rosso | unbranded | unbranded | n/a | 0.9996 |
| American corn Sweet (per piece) | unbranded | unbranded | n/a | 0.9998 |
| Shimeji Mushrooms | unbranded | unbranded | n/a | 0.9990 |
| BOOKLET - LEAVE APPLICATION | unbranded | unbranded | n/a | 0.9967 |
| 7 inch Plate Chuk | unbranded | unbranded | n/a | 0.8480 |
| #_# Prasuma FS Tandoori Veg Momos - Prasuma ⚠ | unbranded | branded | n/a | 0.9998 |
| #_# French Vanilla (500 ml) - Go Zero ⚠ | unbranded | branded | n/a | 0.9983 |
| IDLY RAWA | unbranded | unbranded | n/a | 0.9987 |
| BREAD CRUMBS | unbranded | unbranded | n/a | 0.9997 |
| Air Freshener Godrej ⚠ | unbranded | branded | n/a | 0.9992 |
| Spice-Dhaniya seeds | unbranded | unbranded | n/a | 0.9948 |
| Full Box / Big Box | unbranded | unbranded | n/a | 0.9999 |
| Star Papad ⚠ | unbranded | branded | n/a | 0.7827 |
| Dry Wash Floor mat - Big | unbranded | unbranded | n/a | 0.9993 |
| A4 Sheet | unbranded | unbranded | n/a | 0.9957 |
| #_# Strawberry Kulfi 300gm - Parsi Dairy Farm ⚠ | unbranded | branded | n/a | 1.0000 |
| Golgappa Sooji | unbranded | unbranded | n/a | 0.9996 |
| Pril Liquid ⚠ | unbranded | branded | n/a | 0.9999 |
| RED COLOUR | unbranded | unbranded | n/a | 0.1176 |
| T-shirt - M size | unbranded | unbranded | n/a | 0.9988 |
| Thin Filo Dough For Sweet 450 gms | unbranded | unbranded | n/a | 0.9994 |
| #_# Pink Dome Box 1/2 Kg - Sassy Teaspoon ⚠ | unbranded | branded | n/a | 0.9981 |
| Silicon Dioxide | unbranded | unbranded | n/a | 0.9999 |
| Wild Rocket Micro 100 gm | unbranded | unbranded | n/a | 0.9962 |
| Dried Shiitake mushroom 1kg | unbranded | unbranded | n/a | 0.9988 |
| NONBROMITE BREAD IMPROVER 1 KG 0157 ⚠ | unbranded | branded | n/a | 0.5117 |
| Kombu Leaf Dried 1kg pkt | unbranded | unbranded | n/a | 0.9957 |
| Kiley Soda 250 ML - SNACC ⚠ | unbranded | branded | n/a | 0.5273 |
| #_# Cookies and Cream Ice-cream Tub (100ml) - Meemees ⚠ | unbranded | branded | n/a | 0.9998 |
| Luster Dust Royal Gold ⚠ | unbranded | branded | n/a | 0.0534 |
| Sauce-Peri peri | unbranded | unbranded | n/a | 0.9993 |
| Coriander Green | unbranded | unbranded | n/a | 0.9996 |
| Water Chestnuts | unbranded | unbranded | n/a | 0.9984 |
| Monin Raspberry ⚠ | unbranded | branded | n/a | 0.9999 |
| Vanaspati Ghee nature fresh ⚠ | unbranded | branded | n/a | 0.9969 |
| Polyester Label Sticker (4x2 Inc Red) Non veg | unbranded | unbranded | n/a | 0.9995 |
| Nitrile Hand Gloves (1box = 100 gloves) | unbranded | unbranded | n/a | 0.9995 |
| Pizza Cheese | unbranded | unbranded | n/a | 0.9963 |
| #_# Square Butter Paper - Le Four ⚠ | unbranded | branded | n/a | 0.9450 |
| Sarwar Onion Powder 450gm ⚠ | unbranded | branded | n/a | 0.9999 |
| Veg Spring Roll (pack of 25Pcs) | unbranded | unbranded | n/a | 0.9965 |
| Mdh Dhaniya powder 500gm ⚠ | unbranded | branded | n/a | 1.0000 |
| CREAM | unbranded | unbranded | n/a | 0.9716 |
| Container Paper Printed 250 ML ( dia 116 ) with LID | unbranded | unbranded | n/a | 0.9995 |
| A5 Voucher Leaflet | unbranded | unbranded | n/a | 0.9986 |
| Long Note Book 200 Pgs Chandras SB ⚠ | unbranded | branded | n/a | 0.9948 |
| #_# Modak - Murukku | unbranded | unbranded | n/a | 0.9987 |
| Floor Duster (Pocha) | unbranded | unbranded | n/a | 0.9998 |
| Monin Blue Curaco 700 ml ⚠ | unbranded | branded | n/a | 0.9994 |
| Piri Piri Seasoning | unbranded | unbranded | n/a | 0.9979 |
| Carry Bag Paper 1Kg Printing | unbranded | unbranded | n/a | 0.9995 |
| Hazelnut Brownie Outer Sticker (CBTL) ⚠ | unbranded | branded | n/a | 0.9944 |
| TT RIBBAN J304 (110MM X 300MTR) ⚠ | unbranded | branded | n/a | 0.2814 |
| Sweets Milk Barfi Red Velvet ⚠ | unbranded | branded | n/a | 0.0940 |
| Rich Whipping Cream Gold ⚠ | unbranded | branded | n/a | 0.9979 |
| HALDI POWDER | unbranded | unbranded | n/a | 0.9996 |
| Maggi Cubes Chicken ⚠ | unbranded | branded | n/a | 0.9998 |
| Cake Card 6 | unbranded | unbranded | n/a | 0.9895 |
| Ker Sangri | unbranded | unbranded | n/a | 0.9995 |
| SAKURA DRIED SHITAKE MUSHROOM ⚠ | unbranded | branded | n/a | 0.9985 |
| #_# Tomato Chutney Frozen - Murukku | unbranded | unbranded | n/a | 0.8105 |
| #_# Tar Brush (Dosa Bhatti) | unbranded | unbranded | n/a | 0.9511 |
| RED CABBAGE | unbranded | unbranded | n/a | 0.9999 |
| Fresh Button Mushroom (200GM) | unbranded | unbranded | n/a | 0.9997 |
| Salad Oil 500mL | unbranded | unbranded | n/a | 0.9219 |
| #_# Sticker - Momo Kitchen 40mm - Prasuma ⚠ | unbranded | branded | n/a | 0.9533 |
| Biryani Rice(1121 XXXL) | unbranded | unbranded | n/a | 0.9996 |
| Jain Hing Powder ⚠ | unbranded | branded | n/a | 0.9914 |
| Brown Onion Grinded | unbranded | unbranded | n/a | 0.9993 |
| Pitambari Powder ⚠ | unbranded | branded | n/a | 0.9999 |
| #_# Sticker - Mango Protein Smoothie - The Whole Truth ⚠ | unbranded | branded | n/a | 0.9924 |
| 500 Ml Round Container With Lids (White) | unbranded | unbranded | n/a | 0.9991 |
| Panini Bread Outer Sticker (CBTL) ⚠ | unbranded | branded | n/a | 0.9770 |
| Chicken Tikka filling-Snacc ⚠ | unbranded | branded | n/a | 0.9977 |
| Spray Bottle with Trigger (750 ML) | unbranded | unbranded | n/a | 0.9994 |
| Rice flour Vijay 1KG-SNACC ⚠ | unbranded | branded | n/a | 0.9999 |
| Designer Dummy | unbranded | unbranded | n/a | 0.0210 |
| MONIN HAZELNUT SYRUP 1LTR ⚠ | unbranded | branded | n/a | 1.0000 |
| Carrot Beans Poriyal(ME)-A-BAN | unbranded | unbranded | n/a | 0.7432 |
| Corona Lager Beer 330 ml ⚠ | unbranded | branded | n/a | 0.9997 |
| #_# Misti Doi 100gm - Parsi Dairy Farm ⚠ | unbranded | branded | n/a | 0.9999 |
| Thai Tea Mix 400g packet Chatramue ⚠ | unbranded | branded | n/a | 1.0000 |
| Habit Olives Green Pitted 3Kg ⚠ | unbranded | branded | n/a | 0.9998 |
| 100 ML PAPER  Container | unbranded | unbranded | n/a | 0.9989 |
| Lamb Rack Cap Off 1 Pkt | unbranded | unbranded | n/a | 0.9987 |
| Napkin Bikkgane ⚠ | unbranded | branded | n/a | 0.5078 |
| #_# Sticker - Sauce Dip Sticker Tangy Thai Tom Yum Sauce - Prasuma ⚠ | unbranded | branded | n/a | 0.4610 |
| Cello Tape Green | unbranded | unbranded | n/a | 0.5429 |
| Outer Bag SOS 70 GSM - Snacc ⚠ | unbranded | branded | n/a | 0.8977 |
| Prawns 40/50 C | unbranded | unbranded | n/a | 0.9999 |
| Parry Sugar White ⚠ | unbranded | branded | n/a | 0.9992 |
| Harpic 500 ml ⚠ | unbranded | branded | n/a | 0.9999 |
| Butter Croissant-Snacc ⚠ | unbranded | branded | n/a | 0.7827 |
| ITC Long Note Book 160 pages hard ⚠ | unbranded | branded | n/a | 0.9998 |
| MS FRYPAN 14 | unbranded | unbranded | n/a | 0.9124 |
| Spice-Peri peri seasoning | unbranded | unbranded | n/a | 0.9973 |
| WALNUT | unbranded | unbranded | n/a | 0.9325 |
| BLACK OLIVE 3KG | unbranded | unbranded | n/a | 0.9949 |
| SCOTCH BRITE (4 IN 1) ⚠ | unbranded | branded | n/a | 0.9961 |
| Ketel One Vodka 750 ml ⚠ | unbranded | branded | n/a | 0.9983 |
| GLASS PET 350 - PAPER | unbranded | unbranded | n/a | 0.9005 |
| WALNUT BROKEN 1 KG | unbranded | unbranded | n/a | 0.9996 |
| Laddle Chinese with wooden handle 4 inch | unbranded | unbranded | n/a | 0.9998 |
| Butter Chicken Nuggets | unbranded | unbranded | n/a | 0.9994 |
| Hoegaarden ⚠ | unbranded | branded | n/a | 1.0000 |
| POUCH 200MM X 250MM - Poly Pet - With Barrier (12/70) | unbranded | unbranded | n/a | 0.9991 |
| Oregano Herb 1 Kg | unbranded | unbranded | n/a | 0.9980 |
| Ziplock Bags | unbranded | unbranded | n/a | 0.6002 |
| French Fries 11mm 2.5 Kg | unbranded | unbranded | n/a | 0.9993 |
| COKE CANE ⚠ | unbranded | branded | n/a | 0.0027 |
| Pickle Andhra | unbranded | unbranded | n/a | 0.9654 |
| Kashmiri Mirch Aakhu - Red Chilly Whole Kashmiri | unbranded | unbranded | n/a | 0.9716 |
| Refined Oil | unbranded | unbranded | n/a | 0.9991 |
| #_# Curry Leaves | unbranded | unbranded | n/a | 0.9904 |
| Pizza Platter Butter Paper 16*9 ⚠ | unbranded | branded | n/a | 0.0010 |
| tanquery gin 750 ⚠ | unbranded | branded | n/a | 0.9959 |
| DV Grenadine Syrup 750 ml ⚠ | unbranded | branded | n/a | 0.9983 |
| #_# Chocolate Coated Salted Pistachio Dragees Jar [120 grams] - Entisi Chocolatier ⚠ | unbranded | branded | n/a | 0.9999 |
| Paper Billing Rolls | unbranded | unbranded | n/a | 0.9980 |
| Staff tea | unbranded | unbranded | n/a | 0.9967 |
| Garnish Tray Plastic 9 Insert | unbranded | unbranded | n/a | 0.9901 |
| bakery paper bags | unbranded | unbranded | n/a | 0.9995 |
| Aavin Milk ⚠ | unbranded | branded | n/a | 1.0000 |
| N20 Whipped Cream Chargers ⚠ | unbranded | branded | n/a | 0.0002 |
| WHITE PITTA BREAD (1pcs) | unbranded | unbranded | n/a | 0.9987 |
| Chicken Box (Small) | unbranded | unbranded | n/a | 0.9982 |
| dhaniya whole | unbranded | unbranded | n/a | 0.9998 |
| YU001517 Sensor Magnetiv 2 Nc ⚠ | unbranded | branded | n/a | 0.3277 |
| #_# Frozen Chonk O Rocher - Chonkers ⚠ | unbranded | branded | n/a | 0.7718 |
| Baby Rawas | unbranded | unbranded | n/a | 0.9964 |
| Ghee Pure 500 Ml | unbranded | unbranded | n/a | 0.9955 |
| Sriracha Hot Chilli Sauce Flying Goose 730 gm ⚠ | unbranded | branded | n/a | 1.0000 |
| ANGOSTURA Aromatic bitters (200ML) ⚠ | unbranded | branded | n/a | 0.9999 |
| Purple Cabbage | unbranded | unbranded | n/a | 0.9999 |
| Plum Essence ⚠ | unbranded | branded | n/a | 0.9099 |
| Safed mirchi | unbranded | unbranded | n/a | 0.9978 |
| Royal Challenge ⚠ | unbranded | branded | n/a | 0.9972 |
| Canteen Drink Box (250GSM) SBS ⚠ | unbranded | branded | n/a | 0.0065 |
| Chuk Plate 11 ⚠ | unbranded | branded | n/a | 0.9774 |
| Makhana | unbranded | unbranded | n/a | 0.9997 |
| PP Bag 12x18 Inch | unbranded | unbranded | n/a | 0.9999 |
| #_# Big Bag - Stroopie ⚠ | unbranded | branded | n/a | 0.0331 |
| VKL- Peri Peri Marinade 1Kg ⚠ | unbranded | branded | n/a | 0.9997 |
| Nimbu (Lemon) | unbranded | unbranded | n/a | 0.9996 |
| Black Cardamom 250gm | unbranded | unbranded | n/a | 0.9991 |
| MOTI ELAICHI | unbranded | unbranded | n/a | 0.9983 |
| POCHA (MOP) | unbranded | unbranded | n/a | 0.9803 |
| Bagasse Burger BOX  WIDE BASE | unbranded | unbranded | n/a | 0.9929 |
| Kimirica White Gold Tooth Brush pack ⚠ | unbranded | branded | n/a | 0.9833 |
| #_# Cheese (Melted) - Prasuma ⚠ | unbranded | branded | n/a | 0.9996 |
| Mackeral 6/8 | unbranded | unbranded | n/a | 0.8888 |
| White sesame Seeds 100G - Sancc ⚠ | unbranded | branded | n/a | 0.9998 |
| Mouth Freshner Pkt | unbranded | unbranded | n/a | 0.9974 |
| urad dal | unbranded | unbranded | n/a | 0.9998 |
| Nutrela (1pkt) ⚠ | unbranded | branded | n/a | 0.9992 |
| Paper Printed Kebab Box 6 Compartment | unbranded | unbranded | n/a | 0.9988 |
| CHULLA ⚠ | unbranded | branded | n/a | 0.0119 |
| ROSTED CHANA DAL | unbranded | unbranded | n/a | 0.9979 |
| Finagel ⚠ | unbranded | branded | n/a | 0.9615 |
| Ajwain Whole | unbranded | unbranded | n/a | 0.9973 |
| Moong Dal - Grade 1 (Fine) | unbranded | unbranded | n/a | 0.9983 |
| Paper A4 | unbranded | unbranded | n/a | 0.9991 |
| #_# Cube Pouches - Entisi Chocolatier ⚠ | unbranded | branded | n/a | 0.9995 |
| variyali | unbranded | unbranded | n/a | 0.9967 |
| Danish White Feta 500GM ⚠ | unbranded | branded | n/a | 0.0005 |
| Corrugated Box Small | unbranded | unbranded | n/a | 0.9995 |
| Wooden Spoon (100PCs Each) | unbranded | unbranded | n/a | 0.9979 |
| Gochujang Paste 500gm pkt | unbranded | unbranded | n/a | 0.9888 |
| #_# Eggless Chocolate Chip Pound Cake - Sweetish ⚠ | unbranded | branded | n/a | 0.9752 |
| Elephant Yam | unbranded | unbranded | n/a | 0.9997 |
| Bandan Cap ⚠ | unbranded | branded | n/a | 0.0003 |
| BREAD SANDWICH | unbranded | unbranded | n/a | 0.9955 |
| T65  CAKE FLOUR | unbranded | unbranded | n/a | 0.9878 |
| #_# Naga Chilli Sauce - Prasuma ⚠ | unbranded | branded | n/a | 0.9993 |
| Tata Salt 1kg ⚠ | unbranded | branded | n/a | 1.0000 |
| Kesar Kaju Katli 500 Gms Gold Foil Cover ⚠ | unbranded | branded | n/a | 0.0081 |
| Dust pan (dust pan-20) | unbranded | unbranded | n/a | 0.9944 |
| Mozzarella Cheese - Flanders ⚠ | unbranded | branded | n/a | 0.0770 |
| Colin (Glass Cleaner) ⚠ | unbranded | branded | n/a | 0.9995 |
| Bulgogi Sauce | unbranded | unbranded | n/a | 0.9959 |
| #_# Cone - Dark Chocolate [ 120 ml ] - Getaway ⚠ | unbranded | branded | n/a | 0.9219 |
| TORCH BLOW COOKING ⚠ | unbranded | branded | n/a | 0.0020 |
| T-SHIRT BLACK-L | unbranded | unbranded | n/a | 0.9994 |
| Italian Focassia Polly Bag 8 x 10 Inch | unbranded | unbranded | n/a | 0.9890 |
| Seafood-Basa | unbranded | unbranded | n/a | 0.9971 |
| Basil ⚠ | vegetables | unbranded | n/a | 0.9997 |
| R.O Water Bottles (20 Ltrs) ⚠ | water | unbranded | n/a | 0.9921 |
| STICKERS WVF COLD VARAVRAGE - THINK ORIGINS HAZELNUT COLD FILTER COFFEE FSSAI ⚠ | wvf | branded | n/a | 0.9937 |
| DAILY FRESH MILLETS IDLI AND DOSA BATTER POUCH 1/2KG ⚠ | wvf | branded | n/a | 0.9987 |
| DAILY FRESH SPROUTED PESARATTU BATTER POUCH 1/2KG ⚠ | wvf | branded | n/a | 0.9993 |
| Tawa Roti (7 inch) ⚠ | zomato hyperpure | unbranded | n/a | 0.9974 |
| Rai (Mustard Seed) 100gm ⚠ | zomato hyperpure | unbranded | n/a | 0.9997 |

