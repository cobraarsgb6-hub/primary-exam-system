
// ============================================================
// DYNAMIC PASSAGE LIBRARY (Changes on every exam session!)
// ============================================================

const FANTASY_PASSAGES_POOL = [
  {
    title: 'The City That Waited (Part 6)',
    text: 'The city was a hush. Pale light crept over the cobbles of the deserted square. In the courtyard, the old stone fountain whispered to itself as thin streams of water trickled into the basin. Its white walls glowed like the inside of a seashell in the twilight. High above, the iron gates closed with a mournful sigh, and shadows stretched along the walls, long and thin as fingers. No one walked the silent streets...',
    simile: { phrase: 'glowed like the inside of a seashell', target: 'walls to a seashell' },
    personification: 'The old stone fountain whispered to itself in the courtyard',
    metaphor: { phrase: 'The city was a hush.', meaning: 'The city was completely silent, deserted, and quiet.' },
    vocab: { word: 'cobbles', meaning: 'Rounded stones used to pave historic streets' },
    mood: 'Through silent cobblestones, a whispering fountain, and empty archways'
  },
  {
    title: 'The Whispering Fortress (Part 6)',
    text: 'Silence gripped the fortress like a thick coat of frost. Pale moonlight crawled across the cracked flagstones of the great hall. High above, the iron chandeliers swung gently, groaning in the cold night air. The silver towers gleamed like polished daggers beneath the stars. Below in the dark passage, the freezing mountain wind howled like a hungry wolf. The castle held its breath as midnight struck...',
    simile: { phrase: 'gleamed like polished daggers beneath the stars', target: 'towers to polished daggers' },
    personification: 'The iron chandeliers swung gently, groaning in the cold air',
    metaphor: { phrase: 'Silence was a thick coat of frost.', meaning: 'The cold silence enveloped everything completely and intensely.' },
    vocab: { word: 'flagstones', meaning: 'Large, flat square stones used for paving castle floors' },
    mood: 'Through groaning chandeliers, a howling wind, and cold moonlight'
  },
  {
    title: 'The Sunken Harbor (Part 6)',
    text: 'The harbor was a graveyard of forgotten ships. Thick morning mist crept over the timber planks of the deserted pier. Along the shoreline, the restless waves slapped against the rotting wooden pilings with a low thud. In the distance, the old lighthouse lamp flickered like a dying star in the dark. Overhead, the heavy storm clouds wept soft drops of rain upon the shore. Not a single sailor stirred on the forgotten decks...',
    simile: { phrase: 'flickered like a dying star in the dark', target: 'the lamp to a dying star' },
    personification: 'The heavy storm clouds wept soft drops of rain upon the shore',
    metaphor: { phrase: 'The harbor was a graveyard of forgotten ships.', meaning: 'The harbor was filled with abandoned, decaying wreckage.' },
    vocab: { word: 'pilings', meaning: 'Heavy wooden posts driven into the seabed to support a pier' },
    mood: 'Through weeping clouds, abandoned ships, and flickering lights'
  }
];

const REPORT_PASSAGES_POOL = [
  {
    title: 'Sea Turtles Protection Report',
    text: 'Sea turtles are in danger because people throw plastic and rubbish into the sea. People can stop throwing plastic into the sea and join beach clean-ups. People can also ask boats and ships not to dump rubbish into the ocean. Protecting sea turtles matters because they help keep the ocean healthy. If they disappear, marine ecosystems will suffer greatly.',
    relClause: {
      correct: 'Sea turtles, which are ancient marine reptiles, lay their eggs on sandy beaches.',
      w1: 'Sea turtles which are ancient marine reptiles lay their eggs, on sandy beaches.',
      w2: 'Sea turtles, which are ancient marine reptiles lay their eggs on sandy beaches.',
      w3: 'Sea turtles which are ancient marine reptiles, lay their eggs on sandy beaches.'
    },
    subjectVerb: {
      correct: 'Sea turtles lay their eggs on sandy beaches.',
      wrong: 'Sea turtles lays their eggs on sandy beaches.'
    },
    spelling: {
      prompt: 'If sea turtles ________, marine ecosystems will lose an important species.',
      correct: 'disappear',
      options: ['disappear', 'disapper', 'dissappear', 'dissapper']
    }
  },
  {
    title: 'Coral Reefs Conservation Report',
    text: 'Coral reefs are in grave danger because ocean temperatures are rising and pollution enters coastal waters. People can reduce plastic waste and join coastal conservation programs. Governments can ask large ships not to dump chemicals near reefs. Protecting coral reefs matters because they shelter thousands of marine species. If they disappear, the entire ocean food chain will collapse.',
    relClause: {
      correct: 'Coral reefs, which shelter thousands of marine species, face severe threats from warming oceans.',
      w1: 'Coral reefs which shelter thousands of marine species face severe threats, from warming oceans.',
      w2: 'Coral reefs, which shelter thousands of marine species face severe threats from warming oceans.',
      w3: 'Coral reefs which shelter thousands of marine species, face severe threats from warming oceans.'
    },
    subjectVerb: {
      correct: 'Coral polyps build massive limestone reefs over centuries.',
      wrong: 'Coral polyps builds massive limestone reefs over centuries.'
    },
    spelling: {
      prompt: 'If delicate coral reefs ________, marine biodiversity will be lost.',
      correct: 'disappear',
      options: ['disappear', 'disapper', 'dissappear', 'dissapper']
    }
  }
];

const ARABIC_PASSAGES_POOL = [
  {
    title: 'إدارة الوقت وتنظيم الأولويات (سلاح التلميذ)',
    text: 'الوقتُ كنزٌ ثمينٌ وعطاءٌ إلهي عظيم، والنجاحُ في الحياة لا يتحقق بالأماني، وإنما بحسن إدارة يومنا وترتيب أولوياتنا. يتطلب إنجاز المهام وقتاً محدداً وتركيزاً حثيثاً، والبدء بالأهم قبل المهم. كما يحذر الخبراء من تبديد الوقت في المشتتات وتأجيل عمل اليوم إلى الغد، فالأشخاص الذين ينظمون أوقاتهم هم الأكثر قدرة على تحقيق طموحاتهم وخدمة وطنهم.',
    vocab: { word: 'إنجاز', s: 'يتطلب إنجاز الأعمال تخطيطاً مستمراً', meaning: 'إتمام وتحقيق بنجاح' },
    antonym: { word: 'تأجيل', meaning: 'تعجيل وتبكير' },
    nakiraWord: 'كنزٌ',
    maarefaWord: 'الوقتُ'
  },
  {
    title: 'العمل الجاد وبناء الحضارات (سلاح التلميذ)',
    text: 'العملُ شرفٌ لكل إنسانٍ، وأساسٌ متينٌ لبناء الحضارات وتقدم الأمم والشعوب. لا يتأخر المخلصون عن أداء واجباتهم نحو وطنهم العزيز، ويبذلون قصارى جهدهم في ميادين الإنتاج والمعرفة. إن الفلاح في حقله والعامل في مصنعه كلاهما يسعى لرفعة مصرنا الغالية. فمن يسأل عن سر النهضة يجد أن الإتقان والصبر هما المفتاح الحقيقي لتحقيق المعجزات.',
    vocab: { word: 'قصارى جهدهم', s: 'يبذل المخلصون قصارى جهدهم في العمل', meaning: 'أقصى غاية وسعهم وطاقتهم' },
    antonym: { word: 'يتأخر', meaning: 'يتباكر ويتسارع' },
    nakiraWord: 'شرفٌ',
    maarefaWord: 'العملُ'
  },
  {
    title: 'القراءة ومصادر المعرفة (سلاح التلميذ)',
    text: 'القراءةُ نافذةٌ رحبةٌ يطل منها العقلُ على فضاءات العلم والحكمة. حينما يتأمل الإنسان في صفحات الكتب، يكتشف أفكاراً ملهمة وتجارب تثري حياته وفكره. يتطلب الاستيعاب الجيد تركيزاً حثيثاً وتدويناً للفوائد، دون تسرع أو إهمال. فالأذكياء يستثمرون ساعات فراغهم في المطالعة، لأن العلم رأسُ مالٍ عظيم وسلاحٌ لا يصدأ.',
    vocab: { word: 'حثيثاً', s: 'يتطلب الاستيعاب تركيزاً حثيثاً ومستمراً', meaning: 'سريعاً وجاداً ودقيقاً' },
    antonym: { word: 'إهمال', meaning: 'عناية واهتمام' },
    nakiraWord: 'نافذةٌ',
    maarefaWord: 'القراءةُ'
  }
];
