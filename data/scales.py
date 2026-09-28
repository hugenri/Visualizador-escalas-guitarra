from domain.scale import Scale

SCALES={
"major":Scale("major","Mayor",(0,2,4,5,7,9,11)),
"natural_minor":Scale("natural_minor","Menor natural",(0,2,3,5,7,8,10)),
"harmonic_minor":Scale("harmonic_minor","Menor armónica",(0,2,3,5,7,8,11)),
"melodic_minor":Scale("melodic_minor","Menor melódica",(0,2,3,5,7,9,11)),
"major_pentatonic":Scale("major_pentatonic","Pentatónica mayor",(0,2,4,7,9)),
"minor_pentatonic":Scale("minor_pentatonic","Pentatónica menor",(0,3,5,7,10)),
"blues":Scale("blues","Blues",(0,3,5,6,7,10)),
"dorian":Scale("dorian","Dórica",(0,2,3,5,7,9,10)),
"phrygian":Scale("phrygian","Frigia",(0,1,3,5,7,8,10)),
"lydian":Scale("lydian","Lidia",(0,2,4,6,7,9,11)),
"mixolydian":Scale("mixolydian","Mixolidia",(0,2,4,5,7,9,10)),
"locrian":Scale("locrian","Locria",(0,1,3,5,6,8,10)),
}
