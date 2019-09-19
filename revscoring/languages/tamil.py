from .features import RegexMatches

name = "tamil"

'''
try:
    import enchant
    dictionary = enchant.Dict("ta")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ta'.  " +
                      "Consider installing 'aspell-ta'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "ta". Provided by `aspell-ta`.
"""
'''

badword_regexes = [
    r"ஆபாசச்சொல்",
    r"ஊம்ப",
    r"ஊம்பு",
    r"ஒக்காளி",
    r"ஒத்தா",
    r"ஒம்மால",
    r"ஓ(ல்|ழ்)மாரி",
    r"ஓ(ல்|ழ்|லு|ழு|ழி)",
    r"ஓத்தவன்",
    r"ஓத்தா?",
    r"ஓப்பான்",
    r"ஓலு",
    r"ஓல்",
    r"கிழி",
    r"கூதி",
    r"கை அடிச்சு",
    r"கைஅடி",
    r"சுண்ணி",
    r"சுன்னி",
    r"சூத்த",
    r"சூத்து",
    r"செக்ஸ்கதைகள்",
    r"செக்ஸ்படம்",
    r"தாயோளி",
    r"தே(வ|வு)டியா(ள்)",
    r"பாலச்கரம்",
    r"புண்(ட|டை)",
    r"புண்ட",
    r"புண்டநக்கி",
    r"புண்டை",
    r"புழுத்தி",
    r"பூ(ல்|லு)",
    r"பெண்குறி",
    r"பொச்சு",
    r"மயிருபிடுங்கி",
    r"மயிர்",
    r"முட்டாள்",
    r"முண்(டை|ட)",
    r"முலை",
    r"யோனி",
    r"வல்லுறவு",
    r"வாய்அடி",
    r"விந்து",
    r"aayava ootha alla sunni",  # granny fucking cock
    r"akkula thukki kami di",  # lift your hand and show
    r"alugina papali",  # rotten pussy
    r"amarjith",  # bloody kundi
    r"anaathai kaluthai",  # orphaned donkey
    r"arivu ketta koothi",  # retarded cunt
    r"arippu edutha kuthi mavale",  # the itching pussy
    r"auvusaari koodi",  # prostitute's cunt
    r"avuthu kami",  # remove and show your pussy
    r"baadu",  # pimp
    r"blousei thukkudy",  # lift the blouse and show
    r"chunni",  # dick
    r"enna oombuda elvedutha koodi",  # suck me you dead pussy
    r"ennoda poola oombuda",  # suck my dick
    r"erumbu",  # tits
    r"gajak kol",  # big cock
    r"hakka kudi",  # your sisters cunt
    r"kaai( (adithal|amuki))?",  # boob, caressing boobs, presses the breast
    r"kadiki",  # one who bites the penis
    r"kala viridi",  # wide open the legs
    r"kaluthae",  # donkey
    r"kandaara oli",  # whore
    r"kanji",  # cum
    r"karung kuthi mavale",  # girl having black cunt
    r"keeshan appa",  # a discrimination to human
    r"kena punda",  # stupid cunt
    r"ki adi",  # masturbate
    # cunt; pussy, -face, -hair, -sucker
    r"koo(dhi|thi)( (payale|mayir|nuckie))?",
    r"kudiya baadu",  # cunt boob fucker
    r"kundi",  # ass
    r"kunji payalae",  # cock heaf
    r"kusu koodhi",  # farting cunt
    r"kuthi mudiya thadavi kami di",  # rub your pussy hair and show
    r"kuthi kolutha thevdia",  # prostitute whose pussy is big
    r"kuthia virikira thevdia",  # prostitute who opens her pussy
    r"loosu koodhi",  # fool ass
    r"mairu pudungi",  # pubic hair plucker
    r"makki punda",  # rotting cunt
    r"mayire",  # private part hair
    r"mayiru poodunghi",  # hair plucker
    r"mola sappi",  # person who sucks nipple
    r"molai",  # nipples
    r"molaikku naduvule uttu okka",  # fuck between the boobs
    r"molaikku naduvule utu olu da",  # fuck between the boobs
    r"mollamaari",  # stupid person
    r"monna naaye",  # blunt dog
    r"mukree Chodho",  # mothers puss
    r"munni thalai",  # nipple head
    r"muttaa koodhi",  # stupid cunt
    r"naara koodhi",  # stinking cunt
    r"naara kudhi pethadha",  # born out of a stinky pussy
    r"naii",  # dog
    r"nalla thukki kami di nara kuthia",  # lift and show the smelling pussy
    r"nayee soothile un kunji",  # your dick in dogs ass
    r"oakka utta baadu",  # equivalent to pimp
    r"okkala oli",  # fuck your sister
    r"okkala ozhi",  # fuck your sister
    r"oli the bengali",  # fuck of the bengal
    r"olmaari",  # fucking gigalo
    r"olutha pundai",  # cunt which is oozing out cum
    r"ommala( okka)?",  # your mom
    r"ongaka pundek",  # your sisters cunt
    r"ongappan pundai",  # the cunt which belongs to ur dad
    r"oogili",  # raping immortal stalker
    r"oombu",  # suck
    r"oor othe thevidiya",  # whole town fucks u...
    r"oor thevidya",  # bitch of the city
    r"oore otha thevadiya",  # fucks everyone in town
    r"otha",  # fuck your mom
    r"oththa",  # fuck you
    r"paal pappaali",  # milky boob
    r"paaladanja papali punda",  # haunted pussy
    r"pacha thevdia",  # woman who fucks everyone
    r"pae punda",  # big cunt
    r"pandi un kunjila addi",  # tamilan who fuck his mother
    r"panni soothula currenta vekka",  # electrocuting a pigs asshole
    r"pavadaiya thukki kami di",  # lift the under garment and show
    r"panni",  # pig
    r"papali",  # pussy
    r"parapunda maune",  # son of a beggar's dog
    r"pareh theyvidiya",  # bitch
    r"paruthesi",  # a swear
    r"patcha thevidiya",  # wholly whore
    r"pee thinnu",  # eat shit
    r"pisasu",  # devil/ also a swear
    r"pochchu",  # pussy
    r"pool payya",  # stupid dick
    r"poolu( aruntha punda mavan)?",  # dick
    r"pottachi bonthule okkuria",  # fuck in her pussy
    r"praana kudi",  # nerd , geek , jackass ,
    r"preshaan",  # gay boy with vagina
    r"pullu sappi",  # cock sucker
    r"puluthi( (kami|vudu di))?",  # pull the skin down and show
    r"puluthina poola umbudi",  # suck the peel off dick
    r"punda mavale",  # daughter of cunt
    r"punda mavanae",  # a guy having vagina
    r"punda vaaya",  # cunt mouth
    r"pundaa navane",  # son of a cunt
    r"pundai nakki",  # person who licks pussy
    r"pundaye nakku",  # duck a pussy
    r"pundek leh nandu kadikeh",  # crab bite your cunt
    r"rajeena",  # dumb shit
    r"rose bud",  # head of the penis
    r"saapa naaye",  # flat dog
    r"sakkilia koodhi",  # downcaste asshole
    r"sandhana thaayoli",  # sandalwood motherfucker
    r"sappi",  # penis sucker
    r"selayai thukkudi",  # lift the saree and show
    r"seniyan",  # bad luck/ also a swear
    r"somba koodhi",  # useless cunt
    r"soora koodhi",  # disgraced cunt
    r"soothu",  # ass
    r"soru thunriya illa pee thunriya",  # eating food or dung
    r"sunni( (oombi aaya koodi|umbi))?",  # penis, -suckin cunt, -sucks dick
    r"sunniya oombu",  # suck the dick
    r"sunniya uruvudi thevdia",  # pull the dick you prostitute
    r"suthu kolutha thatuvani",  # prostitute having a big ass
    r"thaanoombi thevidiya paiyan",  # auto fellatio son of a bitch
    r"thambi",  # penis
    r"thatuvani kuthi",  # prostitute cunt
    r"thaii olee mavane",  # mother fucker
    r"thanga thevdia",  # prostitute who wears gold
    r"thatuvani munda",  # prostitute
    r"thatuvani punda",  # whore's cunt
    r"thayoli machbhaat",  # motherfucker bengali
    r"thenu olukkura punda mavale",  # make juice flow from pussy
    r"thevadiya mavan",  # son of a bitch
    r"thevdiya", r"thevidiya",  # prostitute
    r"thonguna mammu naranna koodhi",  # hanging boobs stinking pussy
    r"thoomiya kudiki",  # drink female menstrual blood
    r"thoronthu kami di",  # open and show your pussy
    r"thotti",  # bad man/criminal
    r"thukki kami",  # lift and show
    r"un sooththula en poolu",  # my dick in your ass
    r"un vaila uttu okka",  # fuck in your mouth
    r"unga aaya kuthi",  # your grandmas cunt
    r"unga aya kudi aluku padi",  # parts of the grandmas ass
    r"ungakkala okka",  # fuck your sister
    r"vaile utu okka",  # fuck in your mouth
    r"vaile vatchuko",  # keep it in your mouth
    r"vallaipalam",  # penis
    r"vesai",  # slut/whore
    r"viricha kuthi",  # opened pussy
    r"yethava",  # bastard
    r"yirichi kami"  # open and show pussy
]

badwords = RegexMatches(name + ".badwords", badword_regexes,
                        wrapping=(r"^|[^\w\u0b80-\u0bff]",
                                  r"$|[^\w\u0b80-\u0bff]"))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"பொட்டை"
]

informals = RegexMatches(name + ".informals", informal_regexes,
                         wrapping=(r"^|[^\w\u0b80-\u0bff]",
                                   r"$|[^\w\u0b80-\u0bff]"))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
