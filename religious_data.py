# religious_data.py
# Contains all constant names for Nakshatra, Rashi, Tithi, Yoga, Weekdays

NAKSHATRA_NAMES = {
    0: {
        "english": "Ashwini", 
        "hindi": "अश्विनी", 
        "sanskrit": "अश्विनी",
        "deity": "Ashwini Kumaras",
        "symbol": "Horse's Head",
        "lord": "Ketu"
    },
    1: {
        "english": "Bharani",
        "hindi": "भरणी",
        "sanskrit": "भरणी",
        "deity": "Yama",
        "symbol": "Yoni (Vulva)",
        "lord": "Venus"
    },
    2: {
        "english": "Krittika",
        "hindi": "कृत्तिका",
        "sanskrit": "कृत्तिका",
        "deity": "Agni",
        "symbol": "Razor/Flame",
        "lord": "Sun"
    },
    3: {
        "english": "Rohini",
        "hindi": "रोहिणी",
        "sanskrit": "रोहिणी",
        "deity": "Brahma/Prajapati",
        "symbol": "Chariot/Cart",
        "lord": "Moon"
    },
    4: {
        "english": "Mrigashira",
        "hindi": "मृगशिरा",
        "sanskrit": "मृगशिरा",
        "deity": "Soma/Chandra",
        "symbol": "Deer's Head",
        "lord": "Mars"
    },
    5: {
        "english": "Ardra",
        "hindi": "आर्द्रा",
        "sanskrit": "आर्द्रा",
        "deity": "Rudra",
        "symbol": "Teardrop/Diamond",
        "lord": "Rahu"
    },
    6: {
        "english": "Punarvasu",
        "hindi": "पुनर्वसु",
        "sanskrit": "पुनर्वसु",
        "deity": "Aditi",
        "symbol": "Bow and Quiver",
        "lord": "Jupiter"
    },
    7: {
        "english": "Pushya",
        "hindi": "पुष्य",
        "sanskrit": "पुष्य",
        "deity": "Brihaspati",
        "symbol": "Cow's Udder/Lotus",
        "lord": "Saturn"
    },
    8: {
        "english": "Ashlesha",
        "hindi": "आश्लेषा",
        "sanskrit": "आश्लेषा",
        "deity": "Nagas (Serpents)",
        "symbol": "Coiled Serpent",
        "lord": "Mercury"
    },
    9: {
        "english": "Magha",
        "hindi": "मघा",
        "sanskrit": "मघा",
        "deity": "Pitris (Ancestors)",
        "symbol": "Royal Throne",
        "lord": "Ketu"
    },
    10: {
        "english": "Purva Phalguni",
        "hindi": "पूर्व फाल्गुनी",
        "sanskrit": "पूर्वफाल्गुनी",
        "deity": "Bhaga",
        "symbol": "Front Legs of Bed/Hammock",
        "lord": "Venus"
    },
    11: {
        "english": "Uttara Phalguni",
        "hindi": "उत्तर फाल्गुनी",
        "sanskrit": "उत्तरफाल्गुनी",
        "deity": "Aryaman",
        "symbol": "Back Legs of Bed",
        "lord": "Sun"
    },
    12: {
        "english": "Hasta",
        "hindi": "हस्त",
        "sanskrit": "हस्त",
        "deity": "Savitar/Surya",
        "symbol": "Hand/Fist",
        "lord": "Moon"
    },
    13: {
        "english": "Chitra",
        "hindi": "चित्रा",
        "sanskrit": "चित्रा",
        "deity": "Tvashtar/Vishwakarma",
        "symbol": "Bright Jewel/Pearl",
        "lord": "Mars"
    },
    14: {
        "english": "Swati",
        "hindi": "स्वाती",
        "sanskrit": "स्वाति",
        "deity": "Vayu",
        "symbol": "Young Sprout/Coral",
        "lord": "Rahu"
    },
    15: {
        "english": "Vishakha",
        "hindi": "विशाखा",
        "sanskrit": "विशाखा",
        "deity": "Indra-Agni",
        "symbol": "Triumphal Arch/Potter's Wheel",
        "lord": "Jupiter"
    },
    16: {
        "english": "Anuradha",
        "hindi": "अनुराधा",
        "sanskrit": "अनुराधा",
        "deity": "Mitra",
        "symbol": "Lotus/Triumphal Archway",
        "lord": "Saturn"
    },
    17: {
        "english": "Jyeshtha",
        "hindi": "ज्येष्ठा",
        "sanskrit": "ज्येष्ठा",
        "deity": "Indra",
        "symbol": "Circular Amulet/Umbrella",
        "lord": "Mercury"
    },
    18: {
        "english": "Moola",
        "hindi": "मूल",
        "sanskrit": "मूल",
        "deity": "Nirriti",
        "symbol": "Bundle of Roots/Lion's Tail",
        "lord": "Ketu"
    },
    19: {
        "english": "Purva Ashadha",
        "hindi": "पूर्व आषाढ़",
        "sanskrit": "पूर्वाषाढा",
        "deity": "Apas (Water)",
        "symbol": "Elephant Tusk/Fan",
        "lord": "Venus"
    },
    20: {
        "english": "Uttara Ashadha",
        "hindi": "उत्तर आषाढ़",
        "sanskrit": "उत्तराषाढा",
        "deity": "Vishvadevas",
        "symbol": "Elephant Tusk/Planks of Bed",
        "lord": "Sun"
    },
    21: {
        "english": "Shravana",
        "hindi": "श्रवण",
        "sanskrit": "श्रवण",
        "deity": "Vishnu",
        "symbol": "Ear/Three Footprints",
        "lord": "Moon"
    },
    22: {
        "english": "Dhanishtha",
        "hindi": "धनिष्ठा",
        "sanskrit": "धनिष्ठा",
        "deity": "Eight Vasus",
        "symbol": "Drum/Flute",
        "lord": "Mars"
    },
    23: {
        "english": "Shatabhisha",
        "hindi": "शतभिषा",
        "sanskrit": "शतभिषा",
        "deity": "Varuna",
        "symbol": "Empty Circle/1000 Flowers",
        "lord": "Rahu"
    },
    24: {
        "english": "Purva Bhadrapada",
        "hindi": "पूर्व भाद्रपद",
        "sanskrit": "पूर्वभाद्रपदा",
        "deity": "Aja Ekapada",
        "symbol": "Front Legs of Funeral Cot/Swords",
        "lord": "Jupiter"
    },
    25: {
        "english": "Uttara Bhadrapada",
        "hindi": "उत्तर भाद्रपद",
        "sanskrit": "उत्तरभाद्रपदा",
        "deity": "Ahir Budhnya",
        "symbol": "Back Legs of Funeral Cot/Twins",
        "lord": "Saturn"
    },
    26: {
        "english": "Revati",
        "hindi": "रेवती",
        "sanskrit": "रेवती",
        "deity": "Pushan",
        "symbol": "Fish/Drum",
        "lord": "Mercury"
    }
}

RASHI_NAMES = {
    0: {
        "english": "Mesha",
        "hindi": "मेष",
        "western": "Aries",
        "symbol": "Ram",
        "element": "Fire",
        "lord": "Mars"
    },
    1: {
        "english": "Vrishabha",
        "hindi": "वृषभ",
        "western": "Taurus",
        "symbol": "Bull",
        "element": "Earth",
        "lord": "Venus"
    },
    2: {
        "english": "Mithuna",
        "hindi": "मिथुन",
        "western": "Gemini",
        "symbol": "Twins",
        "element": "Air",
        "lord": "Mercury"
    },
    3: {
        "english": "Karka",
        "hindi": "कर्क",
        "western": "Cancer",
        "symbol": "Crab",
        "element": "Water",
        "lord": "Moon"
    },
    4: {
        "english": "Simha",
        "hindi": "सिंह",
        "western": "Leo",
        "symbol": "Lion",
        "element": "Fire",
        "lord": "Sun"
    },
    5: {
        "english": "Kanya",
        "hindi": "कन्या",
        "western": "Virgo",
        "symbol": "Maiden",
        "element": "Earth",
        "lord": "Mercury"
    },
    6: {
        "english": "Tula",
        "hindi": "तुला",
        "western": "Libra",
        "symbol": "Scales",
        "element": "Air",
        "lord": "Venus"
    },
    7: {
        "english": "Vrishchika",
        "hindi": "वृश्चिक",
        "western": "Scorpio",
        "symbol": "Scorpion",
        "element": "Water",
        "lord": "Mars"
    },
    8: {
        "english": "Dhanu",
        "hindi": "धनु",
        "western": "Sagittarius",
        "symbol": "Bow",
        "element": "Fire",
        "lord": "Jupiter"
    },
    9: {
        "english": "Makara",
        "hindi": "मकर",
        "western": "Capricorn",
        "symbol": "Crocodile/Sea-Goat",
        "element": "Earth",
        "lord": "Saturn"
    },
    10: {
        "english": "Kumbha",
        "hindi": "कुंभ",
        "western": "Aquarius",
        "symbol": "Water Bearer",
        "element": "Air",
        "lord": "Saturn"
    },
    11: {
        "english": "Meena",
        "hindi": "मीन",
        "western": "Pisces",
        "symbol": "Fish",
        "element": "Water",
        "lord": "Jupiter"
    }
}

TITHI_NAMES = {
    # Shukla Paksha (Waxing/Bright Fortnight) - 1 to 15
    1: {"english": "Pratipada", "hindi": "प्रतिपदा", "sanskrit": "प्रतिपद"},
    2: {"english": "Dwitiya", "hindi": "द्वितीया", "sanskrit": "द्वितीया"},
    3: {"english": "Tritiya", "hindi": "तृतीया", "sanskrit": "तृतीया"},
    4: {"english": "Chaturthi", "hindi": "चतुर्थी", "sanskrit": "चतुर्थी"},
    5: {"english": "Panchami", "hindi": "पंचमी", "sanskrit": "पञ्चमी"},
    6: {"english": "Shashthi", "hindi": "षष्ठी", "sanskrit": "षष्ठी"},
    7: {"english": "Saptami", "hindi": "सप्तमी", "sanskrit": "सप्तमी"},
    8: {"english": "Ashtami", "hindi": "अष्टमी", "sanskrit": "अष्टमी"},
    9: {"english": "Navami", "hindi": "नवमी", "sanskrit": "नवमी"},
    10: {"english": "Dashami", "hindi": "दशमी", "sanskrit": "दशमी"},
    11: {"english": "Ekadashi", "hindi": "एकादशी", "sanskrit": "एकादशी"},
    12: {"english": "Dwadashi", "hindi": "द्वादशी", "sanskrit": "द्वादशी"},
    13: {"english": "Trayodashi", "hindi": "त्रयोदशी", "sanskrit": "त्रयोदशी"},
    14: {"english": "Chaturdashi", "hindi": "चतुर्दशी", "sanskrit": "चतुर्दशी"},
    15: {"english": "Purnima", "hindi": "पूर्णिमा", "sanskrit": "पूर्णिमा"},  # Full Moon
    
    # Krishna Paksha (Waning/Dark Fortnight) - 16 to 30
    16: {"english": "Pratipada", "hindi": "प्रतिपदा", "sanskrit": "प्रतिपद"},
    17: {"english": "Dwitiya", "hindi": "द्वितीया", "sanskrit": "द्वितीया"},
    18: {"english": "Tritiya", "hindi": "तृतीया", "sanskrit": "तृतीया"},
    19: {"english": "Chaturthi", "hindi": "चतुर्थी", "sanskrit": "चतुर्थी"},
    20: {"english": "Panchami", "hindi": "पंचमी", "sanskrit": "पञ्चमी"},
    21: {"english": "Shashthi", "hindi": "षष्ठी", "sanskrit": "षष्ठी"},
    22: {"english": "Saptami", "hindi": "सप्तमी", "sanskrit": "सप्तमी"},
    23: {"english": "Ashtami", "hindi": "अष्टमी", "sanskrit": "अष्टमी"},
    24: {"english": "Navami", "hindi": "नवमी", "sanskrit": "नवमी"},
    25: {"english": "Dashami", "hindi": "दशमी", "sanskrit": "दशमी"},
    26: {"english": "Ekadashi", "hindi": "एकादशी", "sanskrit": "एकादशी"},
    27: {"english": "Dwadashi", "hindi": "द्वादशी", "sanskrit": "द्वादशी"},
    28: {"english": "Trayodashi", "hindi": "त्रयोदशी", "sanskrit": "त्रयोदशी"},
    29: {"english": "Chaturdashi", "hindi": "चतुर्दशी", "sanskrit": "चतुर्दशी"},
    30: {"english": "Amavasya", "hindi": "अमावस्या", "sanskrit": "अमावस्या"}  # New Moon
}

PAKSHA = {
    "shukla": {"english": "Shukla Paksha", "hindi": "शुक्ल पक्ष", "meaning": "Bright Fortnight"},
    "krishna": {"english": "Krishna Paksha", "hindi": "कृष्ण पक्ष", "meaning": "Dark Fortnight"}
}

VARA_NAMES = {
    0: {"english": "Sunday", "hindi": "रविवार", "sanskrit": "Ravivar", "lord": "Sun (Surya)"},
    1: {"english": "Monday", "hindi": "सोमवार", "sanskrit": "Somvar", "lord": "Moon (Chandra)"},
    2: {"english": "Tuesday", "hindi": "मंगलवार", "sanskrit": "Mangalvar", "lord": "Mars (Mangal)"},
    3: {"english": "Wednesday", "hindi": "बुधवार", "sanskrit": "Budhvar", "lord": "Mercury (Budh)"},
    4: {"english": "Thursday", "hindi": "गुरुवार", "sanskrit": "Guruvar", "lord": "Jupiter (Guru)"},
    5: {"english": "Friday", "hindi": "शुक्रवार", "sanskrit": "Shukravar", "lord": "Venus (Shukra)"},
    6: {"english": "Saturday", "hindi": "शनिवार", "sanskrit": "Shanivar", "lord": "Saturn (Shani)"}
}

YOGA_NAMES = {
    0: {"english": "Vishkambha", "hindi": "विष्कम्भ", "nature": "Inauspicious"},
    1: {"english": "Priti", "hindi": "प्रीति", "nature": "Auspicious"},
    2: {"english": "Ayushman", "hindi": "आयुष्मान", "nature": "Auspicious"},
    3: {"english": "Saubhagya", "hindi": "सौभाग्य", "nature": "Auspicious"},
    4: {"english": "Shobhana", "hindi": "शोभन", "nature": "Auspicious"},
    5: {"english": "Atiganda", "hindi": "अतिगण्ड", "nature": "Inauspicious"},
    6: {"english": "Sukarma", "hindi": "सुकर्मा", "nature": "Auspicious"},
    7: {"english": "Dhriti", "hindi": "धृति", "nature": "Auspicious"},
    8: {"english": "Shoola", "hindi": "शूल", "nature": "Inauspicious"},
    9: {"english": "Ganda", "hindi": "गण्ड", "nature": "Inauspicious"},
    10: {"english": "Vriddhi", "hindi": "वृद्धि", "nature": "Auspicious"},
    11: {"english": "Dhruva", "hindi": "ध्रुव", "nature": "Auspicious"},
    12: {"english": "Vyaghata", "hindi": "व्याघात", "nature": "Inauspicious"},
    13: {"english": "Harshana", "hindi": "हर्षण", "nature": "Auspicious"},
    14: {"english": "Vajra", "hindi": "वज्र", "nature": "Inauspicious"},
    15: {"english": "Siddhi", "hindi": "सिद्धि", "nature": "Auspicious"},
    16: {"english": "Vyatipata", "hindi": "व्यतीपात", "nature": "Inauspicious"},
    17: {"english": "Variyan", "hindi": "वरीयान", "nature": "Auspicious"},
    18: {"english": "Parigha", "hindi": "परिघ", "nature": "Inauspicious"},
    19: {"english": "Shiva", "hindi": "शिव", "nature": "Auspicious"},
    20: {"english": "Siddha", "hindi": "सिद्ध", "nature": "Auspicious"},
    21: {"english": "Sadhya", "hindi": "साध्य", "nature": "Auspicious"},
    22: {"english": "Shubha", "hindi": "शुभ", "nature": "Auspicious"},
    23: {"english": "Shukla", "hindi": "शुक्ल", "nature": "Auspicious"},
    24: {"english": "Brahma", "hindi": "ब्रह्म", "nature": "Auspicious"},
    25: {"english": "Indra", "hindi": "इन्द्र", "nature": "Auspicious"},
    26: {"english": "Vaidhriti", "hindi": "वैधृति", "nature": "Inauspicious"}
}

# 60-year cycle names for Samvat years
SAMVAT_YEAR_NAMES = [
    "Prabhava", "Vibhava", "Shukla", "Pramoda", "Prajapati",
    "Angirasa", "Shrimukha", "Bhava", "Yuva", "Dhatri",
    "Ishvara", "Bahudhanya", "Pramathi", "Vikrama", "Vrisha",
    "Chitrabhanu", "Svabhanu", "Tarana", "Parthiva", "Vyaya",
    "Sarvajit", "Sarvadharin", "Virodhin", "Vikrita", "Khara",
    "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukha",
    "Hemalamba", "Vilamba", "Vikarin", "Sharvari", "Plava",
    "Shubhakrit", "Shobhana", "Krodhin", "Vishvavasu", "Parabhava",
    "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodhikrit",
    "Paridhavi", "Pramadin", "Ananda", "Rakshasa", "Anala",
    "Pingala", "Kalayukta", "Siddharthi", "Raudra", "Durmati",
    "Dundubhi", "Rudhirodgarin", "Raktaksha", "Krodhana", "Akshaya"
]

KARANA_NAMES = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"]
