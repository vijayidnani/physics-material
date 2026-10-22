// ============================================================
//  THIS IS THE ONLY FILE YOU EDIT (settings + new chapters)
//
//  Per chapter:
//    slug      folder + file prefix (lowercase, hyphens)
//    title     name shown on the page
//    group     topic heading (same text = same group)
//    main      JEE Main levels uploaded      e.g. [1,2,3,4]
//    adv       JEE Advanced levels uploaded  e.g. [1,2]
//    mainKey   JEE Main levels that also have an answer key
//    advKey    JEE Advanced levels that also have an answer key
//    added     date you added it, "YYYY-MM-DD" (drives the New badge)
//
//  PDF paths are built automatically:
//    pdfs/<slug>/<slug>-main-L1.pdf        (question PDF)
//    pdfs/<slug>/<slug>-main-L1-key.pdf    (answer key)
//    pdfs/<slug>/<slug>-adv-L1.pdf / <slug>-adv-L1-key.pdf
// ============================================================
window.SITE = {
  title: "Physics for JEE",
  teacher: "Vijay Idnani",
  role: "Senior Physics Educator, JEE Main & Advanced",
  newDays: 30,   // a chapter shows the New badge for this many days after "added"
  // Paste your full links. Leave "" to hide a button.
  whatsapp: "https://chat.whatsapp.com/YOUR-GROUP-CODE",
  telegram: "https://t.me/YOUR-CHANNEL-NAME"
};

window.CHAPTERS = [
  //{ slug: "units-and-measurements", title: "Units and Measurements", group: "Mechanics", main: [1,2,3,4], adv: [1,2], mainKey: [1,2,3,4], advKey: [1,2], added: "2026-08-01" },
  { slug: "kinematics",             title: "Kinematics",             group: "Mechanics", main: [1,2,3,4], adv: [],   mainKey: [1,2,3,4],     advKey: [],    added: "2026-10-22" },
  { slug: "laws-of-motion",         title: "Laws of Motion",         group: "Mechanics", main: [1,2,3,4],     adv: [],    mainKey: [],       advKey: [],    added: "2026-10-21" },
    { slug: "circular",         title: "Circular Motion",         group: "Mechanics", main: [1,2,3],     adv: [],    mainKey: [1,2,3],       advKey: [],    added: "2026-10-21" },

  //{ slug: "rotational-motion",      title: "Rotational Motion",      group: "Mechanics", main: [],        adv: [],    added: "2026-10-18" },
  //{ slug: "thermodynamics",         title: "Thermodynamics",         group: "Heat and Thermodynamics", main: [1], adv: [], mainKey: [1], added: "2026-10-05" },
  //{ slug: "electrostatics",         title: "Electrostatics",         group: "Electricity and Magnetism", main: [1,2,3], adv: [1], mainKey: [1,2,3], advKey: [1], added: "2026-10-20" },
  //{ slug: "current-electricity",    title: "Current Electricity",    group: "Electricity and Magnetism", main: [], adv: [], added: "2026-10-20" },
  //{ slug: "ray-optics",             title: "Ray Optics",             group: "Optics", main: [], adv: [] },
  //{ slug: "modern-physics",         title: "Modern Physics",         group: "Modern Physics", main: [], adv: [] }
];    
// ---------- PRACTICE SHEETS ----------
// chapterSheet / chapterKey : true if the chapter-wise sheet / its key is uploaded
// topics: one line per topic.  key: true if a key is uploaded.
// ready: false shows "Coming soon" for a topic you have planned but not uploaded.
// added: "YYYY-MM-DD" drives the New badge.
window.PRACTICE = [
  {
    slug: "kinematics", title: "Kinematics", chapterSheet: true, chapterKey: true, added: "2026-10-20",
    topics: [
      { slug: "kinematics-projectile-motion", title: "Projectile Motion", key: true,  added: "2026-10-20" },
      { slug: "kinematics-relative-motion",   title: "Relative Motion",   key: false, added: "2026-10-12" },
      { slug: "kinematics-graphs",            title: "Motion Graphs",     ready: false }
    ]
  },
  {
    slug: "laws-of-motion", title: "Laws of Motion", chapterSheet: false,
    topics: [
      { slug: "laws-of-motion-friction", title: "Friction", key: true, added: "2026-09-01" }
    ]
  }
];
