"""Spanish-language page: Search Console shows 'abogado de accidentes carro summerville / goose creek' searches with no
Spanish page anywhere among the Summerville firms. One well-built page, in Spanish, with the same facts as the English site."""
from .base import page, A, ext, checks, steps, callout, answer, band, esc
from . import firm
from .local import cite

TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
CAR = firm.CAR

body = (
    answer("Si usted sufrió lesiones en un accidente de carro en Summerville, Goose Creek, North Charleston o en cualquier lugar del Lowcountry por culpa de otro conductor, la aseguradora de ese conductor debe pagar sus gastos médicos, sus salarios perdidos, el daño a su vehículo y su dolor y sufrimiento. Usted no está obligado a dar una declaración grabada a esa aseguradora. La consulta con nosotros es gratis, y no cobramos honorarios a menos que ganemos su caso.", "En pocas palabras")
    + '<h2>Quiénes somos</h2>'
    + '<p>Frost Law Group es un bufete de abogados de Summerville, Carolina del Sur, dirigido por un matrimonio: la abogada Tara Frost, quien fue jueza magistrada del condado de Dorchester, lleva todos los casos de lesiones personales; el abogado Jack Frost, quien fue oficial de policía de Summerville y detective del Sheriff del condado de Charleston durante catorce años, dirige la investigación. Nuestra oficina está en 128 Linwood Lane, en Summerville. Atendemos llamadas de accidentes las 24 horas.</p>'
    + '<p>Hablamos con usted en español con la ayuda de un intérprete profesional en cada reunión y cada llamada, y todos los documentos importantes se le explican en su idioma.</p>'
    + '<h2>Casos que llevamos</h2>'
    + checks([
        f'<b>{A(CAR, "Accidentes de carro")}</b>: choques por alcance, en intersecciones, en la I-26 y la autopista 17-A, con conductores distraídos, ebrios o sin seguro, y choques en que el conductor huyó.',
        f'<b>{A("practice-areas/truck-accidents", "Accidentes de camiones")}</b> de 18 ruedas y vehículos comerciales.',
        f'<b>{A("practice-areas/motorcycle-accidents", "Accidentes de motocicleta")}</b> y de <b>{A("practice-areas/pedestrian-accidents", "peatones y ciclistas")}</b>.',
        f'<b>{A("practice-areas/rideshare-accidents", "Accidentes de Uber y Lyft")}</b>, como pasajero o como otro conductor.',
        f'<b>{A("practice-areas/dog-bites", "Mordeduras de perro")}</b>: en Carolina del Sur el dueño es responsable desde la primera mordedura.',
        f'<b>{A("practice-areas/slip-and-fall", "Caídas")}</b> en tiendas, restaurantes y apartamentos.',
        f'<b>{A("practice-areas/wrongful-death", "Muerte injusta")}</b> de un familiar.',
    ])
    + '<h2>Lo que dice la ley de Carolina del Sur</h2>'
    + steps([
        ("Paga el conductor culpable.", f" Carolina del Sur es un estado de responsabilidad por culpa (“at-fault”). Todo conductor debe tener un seguro de al menos $25,000 por persona y $50,000 por accidente ({cite('min_liability')}), lo cual muchas veces no alcanza para una lesión seria."),
        ("Usted puede recuperar aunque tenga parte de la culpa.", " Siempre que su parte no sea mayor del 50 por ciento. Su compensación se reduce según su porcentaje. Las aseguradoras exageran su culpa; por eso importa reunir las pruebas pronto."),
        ("Si el otro conductor no tiene seguro, su propia póliza paga.", f" La cobertura de conductor sin seguro (UM) es obligatoria en Carolina del Sur ({cite('um')}), y la cobertura de conductor con seguro insuficiente (UIM) se le debe ofrecer. Estas coberturas también protegen a los pasajeros y a los peatones."),
        ("Hay un plazo.", f" Tres años desde el accidente para presentar una demanda ({cite('sol_injury')}); dos años si un vehículo del gobierno o un defecto de la carretera estuvo involucrado. Las pruebas desaparecen mucho antes."),
        ("Su estatus migratorio no le quita el derecho a reclamar.", " Cualquier persona lesionada por la negligencia de otro puede presentar un reclamo en Carolina del Sur. Tratamos su información con confidencialidad."),
    ])
    + '<h2>Qué hacer después de un accidente</h2>'
    + steps([
        ("Llame al 911 y quédese en el lugar.", " Pida el número del reporte y el nombre del oficial. En Summerville responde la policía del pueblo; en la I-26, la Patrulla de Carreteras (Highway Patrol)."),
        ("Vaya al médico el mismo día,", " aunque se sienta bien. Diga que fue un accidente de carro y describa todos sus síntomas."),
        ("Tome fotos de todo:", " los carros, el lugar, sus lesiones, la licencia y la tarjeta de seguro del otro conductor."),
        ("Reporte el accidente a su propia aseguradora,", " pero no dé una declaración grabada a la aseguradora del otro conductor. No firme nada y no acepte un cheque antes de hablar con un abogado."),
        ("Llámenos.", f" La consulta es gratis: {TEL}."),
    ])
    + '<h2>Cómo cobramos</h2>'
    + '<p>Los casos de lesiones se llevan con honorarios de contingencia: usted no paga nada por adelantado, y solo cobramos un porcentaje de lo que recuperamos para usted. Si no recuperamos nada, no nos debe honorarios de abogado. Le explicamos por escrito, en español, cualquier costo del caso antes de que firme.</p>'
    + '<h2>Dónde estamos</h2>'
    + f'<p>{firm.NAME}, {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}. Teléfono: {TEL}. Atendemos a residentes de Summerville, {A("areas/goose-creek", "Goose Creek")}, {A("areas/ladson", "Ladson")}, {A("areas/north-charleston", "North Charleston")}, {A("areas/charleston", "Charleston")}, {A("areas/moncks-corner", "Moncks Corner")} y todo el Lowcountry. Si sus lesiones no le permiten viajar, vamos a su casa o al hospital.</p>'
    + '[[nap]]'
    + '<h2>Consulta gratis</h2><p>Cuéntenos qué pasó. Le diremos con honestidad si tiene un caso, cuánto puede valer y qué hacer ahora. Puede escribir en español.</p>[[form]]'
    + callout("<b>Llame a Frost primero:</b> antes de dar una declaración, firmar un documento o aceptar un cheque de la aseguradora, hable con nosotros. La primera conversación con la aseguradora determina todo lo que sigue.")
    + band("¿Lesionado en un accidente? Llámenos.", "Consulta gratis. No cobramos a menos que ganemos. Atendemos las 24 horas.", primary=("contact", "Consulta gratis"))
)

page("es/abogado-de-accidentes", kind="page", layout="one", lang="es", hub=None, cta=[("contact", "Consulta gratis", "btn"), ("tel:" + firm.PHONE_E164, firm.PHONE, "btn ghost")],
     title="Abogado de Accidentes de Carro en Summerville, SC | Frost Law Group",
     description="¿Lesionado en un accidente de carro en Summerville, Goose Creek o North Charleston? Abogados de accidentes de Frost Law Group. Consulta gratis, no cobramos a menos que ganemos. (843) 419-6653.",
     h1="Abogado de Accidentes de Carro en Summerville, Carolina del Sur", eyebrow="Consulta gratis · No cobramos a menos que ganemos · Atención 24 horas", nav_label="Español",
     lead="Si otro conductor le causó lesiones en Summerville, Goose Creek, North Charleston o en cualquier lugar del Lowcountry, tiene derecho a una compensación. Le explicamos sus derechos en su idioma.",
     summary="Abogados de accidentes en Summerville. Consulta gratis, en español.",
     body=body, priority=0.8,
     faqs=[
         ("¿Cuánto cuesta contratar a un abogado de accidentes?", "Nada por adelantado. Cobramos un porcentaje de lo que recuperamos para usted; si no recuperamos nada, no nos debe honorarios de abogado. La consulta es gratis."),
         ("¿Puedo reclamar si no tengo papeles?", "Sí. Cualquier persona lesionada por la negligencia de otro puede presentar un reclamo en Carolina del Sur, y su información se trata con confidencialidad."),
         ("¿Cuánto tiempo tengo para presentar un reclamo en Carolina del Sur?", "Tres años desde el accidente para la mayoría de los casos; dos años si un vehículo del gobierno o un defecto de la carretera estuvo involucrado. Llame pronto: las pruebas desaparecen en semanas."),
         ("¿Qué pasa si el otro conductor no tiene seguro?", "Su propia póliza tiene cobertura de conductor sin seguro (UM), obligatoria en Carolina del Sur, que paga su reclamo. Si el otro conductor tiene poco seguro, su cobertura UIM paga la diferencia."),
         ("¿Debo hablar con la aseguradora del otro conductor?", "No antes de hablar con un abogado. No está obligado a dar una declaración grabada, y lo que diga se usará para pagarle menos."),
         ("¿Atienden en Goose Creek y North Charleston?", "Sí, en todo el condado de Dorchester, Berkeley, Charleston y Colleton. Si no puede viajar, vamos a su casa o al hospital."),
     ],
     related=[CAR, CAR + "/uninsured-motorist-accidents", "practice-areas/dog-bites"])
