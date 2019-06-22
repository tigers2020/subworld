from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

FLAG = {
    "ae": "U.A.E",
    "af": "Afghanistan",
    "ag": "Antigua",
    "ai": "Anguilla",
    "al": "Albania",
    "am": "Armenia",
    "an": "NetherlandsAntilles",
    "ao": "Angola",
    "ar": "Argentina",
    "as": "AmericanSamoa",
    "at": "Austria",
    "au": "Australia",
    "aw": "Aruba",
    "ax": "AlandIslands",
    "az": "Azerbaijan",
    "ba": "Bosnia",
    "bb": "Barbados",
    "bd": "Bangladesh",
    "be": "Belgium",
    "bf": "BurkinaFaso",
    "bg": "Bulgaria",
    "bh": "Bahrain",
    "bi": "Burundi",
    "bj": "Benin",
    "bm": "Bermuda",
    "bn": "Brunei",
    "bo": "Bolivia",
    "br": "Brazil",
    "bs": "Bahamas",
    "bt": "Bhutan",
    "bv": "BouvetIsland",
    "bw": "Botswana",
    "by": "Belarus",
    "bz": "Belize",
    "ca": "Canada",
    "cc": "CocosIslands",
    "cd": "Congo",
    "cf": "CentralAfricanRepublic",
    "cg": "CongoBrazzaville",
    "ch": "Switzerland",
    "ci": "CoteDivoire",
    "ck": "CookIslands",
    "cl": "Chile",
    "cm": "Cameroon",
    "cn": "China",
    "co": "Colombia",
    "cr": "CostaRica",
    "cs": "Serbia",
    "cu": "Cuba",
    "cv": "CapeVerde",
    "cx": "ChristmasIsland",
    "cy": "Cyprus",
    "cz": "CzechRepublic",
    "de": "Germany",
    "dj": "Djibouti",
    "dk": "Denmark",
    "dm": "Dominica",
    "do": "DominicanRepublic",
    "dz": "Algeria",
    "ec": "Ecuador",
    "ee": "Estonia",
    "eg": "Egypt",
    "eh": "WesternSahara",
    "er": "Eritrea",
    "es": "Spain",
    "et": "Ethiopia",
    "eu": "EuropeanUnion",
    "fi": "Finland",
    "fj": "Fiji",
    "fk": "FalklandIslands",
    "fm": "Micronesia",
    "fo": "FaroeIslands",
    "fr": "France",
    "ga": "Gabon",
    "gbuk": "UnitedKingdom",
    "gbeng": "England",
    "gbsct": "Scotland",
    "gbwls": "Wales",
    "gd": "Grenada",
    "ge": "Georgia",
    "gf": "FrenchGuiana",
    "gh": "Ghana",
    "gi": "Gibraltar",
    "gl": "Greenland",
    "gm": "Gambia",
    "gn": "Guinea",
    "gp": "Guadeloupe",
    "gq": "EquatorialGuinea",
    "gr": "Greece",
    "gs": "SandwichIslands",
    "gt": "Guatemala",
    "gu": "Guam",
    "gw": "Guinea-bissau",
    "gy": "Guyana",
    "hk": "HongKong",
    "hm": "HeardIsland",
    "hn": "Honduras",
    "hr": "Croatia",
    "ht": "Haiti",
    "hu": "Hungary",
    "id": "Indonesia",
    "ie": "Ireland",
    "il": "Israel",
    "in": "India",
    "io": "IndianOceanTerritory",
    "iq": "Iraq",
    "ir": "Iran",
    "is": "Iceland",
    "it": "Italy",
    "jm": "Jamaica",
    "jo": "Jordan",
    "jp": "Japan",
    "ke": "Kenya",
    "kg": "Kyrgyzstan",
    "kh": "Cambodia",
    "ki": "Kiribati",
    "km": "Comoros",
    "kn": "SaintKittsAndNevis",
    "kp": "NorthKorea",
    "kr": "SouthKorea",
    "kw": "Kuwait",
    "ky": "CaymanIslands",
    "kz": "Kazakhstan",
    "la": "Laos",
    "lb": "Lebanon",
    "lc": "SaintLucia",
    "li": "Liechtenstein",
    "lk": "SriLanka",
    "lr": "Liberia",
    "ls": "Lesotho",
    "lt": "Lithuania",
    "lu": "Luxembourg",
    "lv": "Latvia",
    "ly": "Libya",
    "ma": "Morocco",
    "mc": "Monaco",
    "md": "Moldova",
    "me": "Montenegro",
    "mg": "Madagascar",
    "mh": "MarshallIslands",
    "mk": "Macedonia",
    "ml": "Mali",
    "mm": "Burma",
    "mn": "Mongolia",
    "mo": "Macau",
    "mp": "NorthernMarianaIslands",
    "mq": "Martinique",
    "mr": "Mauritania",
    "ms": "Montserrat",
    "mt": "Malta",
    "mu": "Mauritius",
    "mv": "Maldives",
    "mw": "Malawi",
    "mx": "Mexico",
    "my": "Malaysia",
    "mz": "Mozambique",
    "na": "Namibia",
    "nc": "NewCaledonia",
    "ne": "Niger",
    "nf": "NorfolkIsland",
    "ng": "Nigeria",
    "ni": "Nicaragua",
    "nl": "Netherlands",
    "no": "Norway",
    "np": "Nepal",
    "nr": "Nauru",
    "nu": "Niue",
    "nz": "NewZealand",
    "om": "Oman",
    "pa": "Panama",
    "pe": "Peru",
    "pf": "FrenchPolynesia",
    "pg": "NewGuinea",
    "ph": "Philippines",
    "pk": "Pakistan",
    "pl": "Poland",
    "pm": "SaintPierre",
    "pn": "PitcairnIslands",
    "pr": "PuertoRico",
    "ps": "Palestine",
    "pt": "Portugal",
    "pw": "Palau",
    "py": "Paraguay",
    "qa": "Qatar",
    "re": "Reunion",
    "ro": "Romania",
    "rs": "Serbia",
    "ru": "Russia",
    "rw": "Rwanda",
    "sa": "SaudiArabia",
    "sb": "SolomonIslands",
    "sc": "Seychelles",
    "sd": "Sudan",
    "se": "Sweden",
    "sg": "Singapore",
    "sh": "SaintHelena",
    "si": "Slovenia",
    "sj": "JanMayen",
    "sk": "Slovakia",
    "sl": "SierraLeone",
    "sm": "SanMarino",
    "sn": "Senegal",
    "so": "Somalia",
    "sr": "Suriname",
    "st": "SaoTome",
    "sv": "ElSalvador",
    "sy": "Syria",
    "sz": "Swaziland",
    "tc": "CaicosIslands",
    "td": "Chad",
    "tf": "FrenchTerritories",
    "tg": "Togo",
    "th": "Thailand",
    "tj": "Tajikistan",
    "tk": "Tokelau",
    "tl": "Timorleste",
    "tm": "Turkmenistan",
    "tn": "Tunisia",
    "to": "Tonga",
    "tr": "Turkey",
    "tt": "Trinidad",
    "tv": "Tuvalu",
    "tw": "Taiwan",
    "tz": "Tanzania",
    "ua": "Ukraine",
    "ug": "Uganda",
    "um": "UsMinorIslands",
    "us": "UnitedStates",
    "uy": "Uruguay",
    "uz": "Uzbekistan",
    "va": "VaticanCity",
    "vc": "SaintVincent",
    "ve": "Venezuela",
    "vg": "BritishVirginIslands",
    "vi": "UsVirginIslands",
    "vn": "Vietnam",
    "vu": "Vanuatu",
    "wf": "WallisAndFutuna",
    "ws": "Samoa",
    "ye": "Yemen",
    "yt": "Mayotte",
    "za": "SouthAfrica",
    "zm": "Zambia",
    "zw": "Zimbabwe",

}

# Create your models here.
from django.urls import reverse

from search.models import MovieDB, TvSeriesDB


class Country(models.Model):
    name = models.CharField(max_length=128)
    iso_3166_2 = models.CharField(max_length=8)
    additional_aliases = models.CharField(max_length=128, null=True)


class Language(models.Model):
    language_family = models.CharField(max_length=126)
    iso_language_name = models.CharField(max_length=255)
    native_name = models.CharField(max_length=255)
    iso_639_1 = models.CharField(max_length=8)
    iso_639_2_t = models.CharField(max_length=8)
    iso_639_2_b = models.CharField(max_length=8)
    iso_639_3 = models.CharField(max_length=8, null=True)
    notes = RichTextField(null=True)

    def __str__(self):
        return self.iso_language_name + '[' + self.native_name + ']'


class MovieSubtitle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    db_id = models.ForeignKey(MovieDB, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    rate_star = models.IntegerField(default=0)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    downloaded = models.IntegerField(default=0)
    comment = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("subtitle:movie_detail", args=[str(self.db_id.id)])

    class Meta:
        get_latest_by = ["upload_date"]
        ordering = ['-rate_good', '-downloaded']
        indexes = [
            models.Index(fields=['title'], name='movie_title_idx')
        ]


class TvSubtitle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    db_id = models.ForeignKey(TvSeriesDB, on_delete=models.CASCADE)
    season_id = models.IntegerField()
    episode_id = models.IntegerField()
    name = models.CharField(max_length=255)
    sub_file = models.FileField(unique=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    rate_star = models.IntegerField(default=0)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    downloaded = models.IntegerField(default=0)
    comment = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = ["upload_date"]
        ordering = ['season_id', 'episode_id', 'rate_good','-downloaded']
        indexes = [
            models.Index(fields=['name'], name='tv_name_idx')
        ]