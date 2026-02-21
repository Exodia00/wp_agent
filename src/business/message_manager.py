
# todo: internationalization

welcome = "Hello, we are in, "

ask_for_city = "What city are you in?"



def service_selection_get_values(number: str, lang: str = "ar"):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "شنو هي الخدمة اللي باغي؟\n"
                "اختار واحد من هاد الاختيارات:"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "srv_bache_vinyl", "title": "باش / ڤينيل"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "srv_beachflag", "title": "Beach Flag"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "srv_rollup", "title": "Rollup"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "srv_xbanner", "title": "X‑Banner"}
                }
            ]
        }
    else:
        return {
            "to": number,
            "body": (
                "Quel service souhaitez‑vous ?\n"
                "Veuillez choisir une option :"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "srv_bache_vinyl", "title": "Bâche / Vinyl"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "srv_beachflag", "title": "Beach Flag"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "srv_rollup", "title": "Rollup"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "srv_xbanner", "title": "X‑Banner"}
                }
            ]
        }


def bache_vinyl_get_values(number: str, lang: str):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "شحال بغيتي تدير؟\n"
                "اختار واحد من هاد الاختيارات:"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "opt_bache", "title": "باش"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "opt_vinyl", "title": "ڤينيل"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "opt_sticker", "title": "ستيكر"}
                }
            ]
        }
    else:
        return {
            "to": number,
            "body": (
                "Quel type souhaitez‑vous ?\n"
                "Veuillez choisir une option :"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "opt_bache", "title": "Bâche"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "opt_vinyl", "title": "Vinyl"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "opt_sticker", "title": "Sticker"}
                }
            ]
        }



def are_you_in_casa_get_values(number: str, lang: str):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "واش كتوجد فكازا ؟\n"
                "اختار نعم ولا:"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "loc_yes", "title": "نعم"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "loc_no", "title": "لا"}
                }
            ]
        }
    else:
        return {
            "to": number,
            "body": (
                "Êtes‑vous à Casablanca ?\n"
                "Veuillez choisir :"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "loc_yes", "title": "Oui"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "loc_no", "title": "Non"}
                }
            ]
        }



def thank_you_get_values(number: str, lang: str):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "شكراً بزاف على وقتك!\n"
                "غادي يتواصل معاك واحد من الفريق ديالنا قريباً إن شاء الله."
            )
        }
    else:
        return {
            "to": number,
            "body": (
                "Merci pour votre temps !\n"
                "Un membre de notre équipe vous contactera très bientôt."
            )
        }



def ask_dimensions_get_values(number: str, lang: str):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "👌\n"
                "شنو هي الأبعاد اللي بغيتي؟"
            )
        }
    else:
        return {
            "to": number,
            "body": (
                "Parfait ! 👌\n"
                "Quelles dimensions souhaitez‑vous ?"
            )
        }



def activity_selection_get_values(number: str, lang: str):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "مزيان! باش نكمّلو معاك، قول ليا النشاط ديال المشروع ديالك:\n"
                "اختار واحد من هاد الاختيارات:"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "act_edu", "title": "تعليمي"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_location", "title": "كراء السيارات"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_monetique", "title": "خدمات الأداء"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_salon", "title": "صالون تجميل"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_industrial", "title": "صناعي"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_commercial", "title": "تجاري"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_other", "title": "آخر"}
                }
            ]
        }

    else:
        return {
            "to": number,
            "body": (
                "Parfait ! Pour mieux comprendre votre besoin, merci d’indiquer votre activité :\n"
                "Veuillez choisir une option ci‑dessous :"
            ),
            "buttons": [
                {
                    "type": "reply",
                    "reply": {"id": "act_edu", "title": "Éducation"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_location", "title": "Location de voitures"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_monetique", "title": "Monétique"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_salon", "title": "Salon esthétique"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_industrial", "title": "Industriel"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_commercial", "title": "Commercial"}
                },
                {
                    "type": "reply",
                    "reply": {"id": "act_other", "title": "Autre"}
                }
            ]
        }



def final_thank_you_with_assets_get_values(number: str, lang: str):
    if lang == "ar":
        return {
            "to": number,
            "body": (
                "شكراً بزاف على وقتك!\n"
                "واحد من الفريق ديالنا غادي يتاصل بيك قريباً إن شاء الله.\n\n"
                "إلا كان عندك شي صور، لوغو، نصوص، أفكار، أو أي تفاصيل بغيتي ندمجوهم فالتصميم، "
                "مرحبا تبعتيهم هنا فالمحادثة باش نقدرو نخدمو بيهم."
            )
        }
    else:
        return {
            "to": number,
            "body": (
                "Merci pour votre temps !\n"
                "L’un de nos agents vous contactera très bientôt.\n\n"
                "Si vous avez des images, logos, textes, idées ou tout autre élément que vous souhaitez "
                "inclure dans le design, n’hésitez pas à les envoyer directement dans cette conversation "
                "afin que nous puissions les utiliser."
            )
        }


def welcome_get_service(lang):
    if lang == "fr" :
        return "frensh get service"
    else :
        return "arabic get service"




def welcome_get_lang_values(number: str):
    return {
        "to": number,
        "body": (
            "Bonjour, merci de nous avoir contactés !\n"
            "Salut! شكراً بزاف على تواصلك معانا.\n\n"
            "Nous sommes une entreprise de design graphique située ici : <votre lien>\n"
            "حنا شركة ديال الديزاين الكرافيكي، والمحل ديالنا كاين فـ الدار البيضاء، حي الأزهر البرنوصي: <الرابط>\n\n"
            "Veuillez choisir votre langue préférée :\n"
            "اختار اللغة اللي بغيتي :"
        ),
        "buttons": [
            {
                "type": "reply",
                "reply": {"id": "lang_ar", "title": "العربية (الدارجة)"}
            },
            {
                "type": "reply",
                "reply": {"id": "lang_fr", "title": "Français"}
            }
        ]
    }



