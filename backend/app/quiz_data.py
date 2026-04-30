from .models import Question


QUESTION_BANK = [
    Question(id="q01", prompt="I usually look for the deeper meaning before I act.", weights={"Ni": 2.0, "Ne": 0.5}, tags=["core", "perceiving", "ni-ne"]),
    Question(id="q02", prompt="I enjoy exploring many different ideas before choosing one.", weights={"Ne": 2.0, "Ni": 0.5}, tags=["core", "perceiving", "ni-ne"]),
    Question(id="q03", prompt="I trust what has worked before more than trying something new.", weights={"Si": 2.0, "Ni": 0.5}, tags=["core", "perceiving", "si-se"]),
    Question(id="q04", prompt="I like responding to what is happening right now.", weights={"Se": 2.0, "Ne": 0.5}, tags=["core", "perceiving", "si-se"]),
    Question(id="q05", prompt="I want my decisions to make clear logical sense.", weights={"Ti": 2.0, "Te": 0.5}, tags=["core", "judging", "ti-te"]),
    Question(id="q06", prompt="Getting practical results matters more to me than perfect logic.", weights={"Te": 2.0, "Ti": 0.5}, tags=["core", "judging", "ti-te"]),
    Question(id="q07", prompt="I choose based on what feels personally right to me.", weights={"Fi": 2.0, "Fe": 0.5}, tags=["core", "judging", "fi-fe"]),
    Question(id="q08", prompt="I notice how other people feel and adjust to keep the mood good.", weights={"Fe": 2.0, "Fi": 0.5}, tags=["core", "judging", "fi-fe"]),
    Question(id="q09", prompt="I often turn a messy situation into one main takeaway.", weights={"Ni": 2.0, "Ti": 0.5}, tags=["core", "ni-ne"]),
    Question(id="q10", prompt="One idea usually leads me to several more.", weights={"Ne": 2.0, "Ti": 0.5}, tags=["core", "ni-ne"]),
    Question(id="q11", prompt="Routine and familiar methods help me do my best work.", weights={"Si": 2.0, "Te": 0.5}, tags=["core", "si-se"]),
    Question(id="q12", prompt="I learn best by jumping in and trying it for myself.", weights={"Se": 2.0, "Te": 0.5}, tags=["core", "si-se"]),
    Question(id="q13", prompt="I enjoy breaking ideas down until they fully make sense.", weights={"Ti": 2.0, "Ni": 0.5}, tags=["core", "ti-te"]),
    Question(id="q14", prompt="I naturally organize people or tasks to keep things moving.", weights={"Te": 2.0, "Se": 0.5}, tags=["core", "ti-te"]),
    Question(id="q15", prompt="I hold onto what feels true to me, even if I cannot explain it well.", weights={"Fi": 2.0, "Ni": 0.5}, tags=["core", "fi-fe"]),
    Question(id="q16", prompt="I can usually tell what kind of emotional support a group needs.", weights={"Fe": 2.0, "Ne": 0.5}, tags=["adaptive", "fi-fe"]),
    Question(id="q17", prompt="I would rather follow one clear vision than keep every option open.", weights={"Ni": 2.0, "Te": 0.5}, tags=["adaptive", "ni-ne"]),
    Question(id="q18", prompt="New ideas excite me even before I know if they are useful.", weights={"Ne": 2.0, "Fi": 0.5}, tags=["adaptive", "ni-ne"]),
    Question(id="q19", prompt="I often rely on memory and past experience when deciding what to do.", weights={"Si": 2.0, "Fi": 0.5}, tags=["adaptive", "si-se"]),
    Question(id="q20", prompt="I act quickly when I notice an opening in the moment.", weights={"Se": 2.0, "Fe": 0.5}, tags=["adaptive", "si-se"]),
    Question(id="q21", prompt="An idea is not useful to me unless it holds up under close testing.", weights={"Ti": 2.0, "Si": 0.5}, tags=["adaptive", "ti-te"]),
    Question(id="q22", prompt="I am comfortable setting goals and expecting people to meet them.", weights={"Te": 2.0, "Ni": 0.5}, tags=["adaptive", "ti-te"]),
    Question(id="q23", prompt="I notice quickly when something feels wrong, even if it looks successful.", weights={"Fi": 2.0, "Si": 0.5}, tags=["adaptive", "fi-fe"]),
    Question(id="q24", prompt="I often feel responsible for the emotional tone around me.", weights={"Fe": 2.0, "Si": 0.5}, tags=["adaptive", "fi-fe"]),
    Question(id="q25", prompt="I care more about what something means than what it looks like on the surface.", weights={"Ni": 2.0, "Fi": 0.5}, tags=["adaptive", "ni-ne"]),
    Question(id="q26", prompt="Talking through ideas usually gives me even more ideas.", weights={"Ne": 2.0, "Fe": 0.5}, tags=["adaptive", "ni-ne"]),
    Question(id="q27", prompt="I prefer steady, reliable methods over making it up as I go.", weights={"Si": 2.0, "Ti": 0.5}, tags=["adaptive", "si-se"]),
    Question(id="q28", prompt="I notice what is going on around me before I start analyzing it.", weights={"Se": 2.0, "Ti": 0.5}, tags=["adaptive", "si-se"]),
    Question(id="q29", prompt="I would rather understand why something works than just use the fastest method.", weights={"Ti": 2.0, "Ne": 0.5}, tags=["adaptive", "ti-te"]),
    Question(id="q30", prompt="I can put my feelings aside to do what works best.", weights={"Te": 2.0, "Se": 0.5}, tags=["adaptive", "ti-te"]),
]


BASE_QUESTION_IDS = [question.id for question in QUESTION_BANK[:15]]
