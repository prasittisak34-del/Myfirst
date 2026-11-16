# Agent prompt template: White mascot fitness explainer (Google Flow)

วิธีใช้: แก้ STEP 2 (พร็อพ) กับ STEP 3 (ฉาก) ให้ตรงกับเรื่องใหม่ (ท่าตัวละคร STEP 1 ใช้ซ้ำได้เกือบทั้งหมด เพิ่ม/ลดได้)
ก๊อปตั้งแต่เส้นด้านล่างไปวางในเอเจนต์ แล้วแนบรูปทั้งหมดในโฟลเดอร์ style-ref/ ของสกิล (EYE-REF.png + ภาพที่เราเคยสร้าง) ไปด้วยทุกครั้ง
ห้ามใช้เฟรมจากคลิปอ้างอิงของคนอื่นเป็น style ref อีก

---

## ROLE
You are an image generation agent working in Google Flow. You produce every image listed below for a 16:9 Thai fitness-knowledge YouTube video ("Why you train hard but your muscles don't grow: sleep"). The editor builds every shot in LAYERS: an empty background plate + a character cut-out on top, so the editor can zoom in/out and slide the character into the scene separately. Clean cut-outs and empty plates matter more than anything else.

## CRITICAL RULES
1. Generate EVERYTHING in this list in ONE run. Never stop to ask questions, never wait for approval, never skip an item. If something fails, retry it, then continue.
2. Character poses (C-items) and props (R-items): render on a PURE FLAT GREEN background #00FF00, the whole body/object in frame with ~8% margin, no floor, no cast shadow on the background, no reflections, no text, no watermark, no border.
3. Background plates (B-items): 16:9 (1920x1080 or larger), completely EMPTY of people and characters, nothing important in the lower-middle area where the character will stand, no text.
4. ONE character only, the same in every image: keep the exact same head shape, eye shape, body proportions, wristbands and shorts in every pose (use C01 as the ingredient image for all other poses).
5. No readable text anywhere (phones, papers, clocks, labels stay blank or show simple symbols only). The editor adds Thai text later.
6. STYLE REFERENCES: the attached images in style-ref/ are OUR OWN earlier results. Match them exactly: EYE-REF.png + C01/C03/C07/C09/C11 for the character, B01/B02/B06/B08 for the background painting style, R04/R06/R11 for props. Use new rooms/props for this topic, but the same look.
7. EYES (most important, check every image): the character ALWAYS has exactly the eyes in EYE-REF.png: two solid matte BLACK vertical ovals (height about 1.6x width), same size, placed side by side at the same height in the middle of the face, spaced about one eye-width apart, both looking straight ahead in the same direction. No pupils, no white sclera, no eyelids, no eyebrows, no highlights, no glow, no colour. Do NOT change the eye shape for emotions (no arcs, no lines, no crosses, no wide circles, no squints, no tilted eyes); show emotion ONLY with body pose, head tilt and hands. Exception only for a sleeping pose: the same two ovals made shorter and flatter (closed), still black and the same position. If both eyes are not the same black ovals pointing the same way, redo the image.
8. BACKGROUND PLATES must be in the SAME CARTOON STYLE as B01/B02/B06/B08: clean 2D cartoon / anime background painting with dark ink outlines on every object, flat cel colours with soft gradients, simple shapes, no photo realism, no 3D render look, no photo textures. Never put posters, paintings, TV screens or photos showing a person or character on the walls (keep frames empty or with a simple landscape).
9. Output files named exactly by ID (C01.png, R05.png, B03.png). PNG, at least 1536 px on the long side. No videos.

## GLOBAL STYLE
THE CHARACTER ("White"):
- An athletic muscular humanoid made of smooth matte WHITE material (very light warm white #F4F2EE with soft light-grey cel shading to show the muscles: chest, abs, shoulders, arms, calves). Fit gym body, strong but not a huge bodybuilder.
- Head: smooth tall ROUNDED egg-shaped head (no ears, no hair, no nose, NO MOUTH), exactly like EYE-REF.png. Eyes: see rule 7 (two identical solid black vertical ovals, never changed by emotion).
- Wears only: plain CHARCOAL-BLACK athletic shorts and one thin BLACK wristband on each wrist. Barefoot, simple feet.
- Line work: clean dark-grey outline (#3A3A3A) around the whole silhouette and main muscle lines so the white body reads clearly on light backgrounds. Clean modern manga / cel-shaded illustration, NOT 3D render, NOT plastic, NOT photo.
PROPS: same illustration style (clean outline + cel shading), chunky readable shapes, readable at small size.
BACKGROUND PLATES: clean 2D cartoon background painting exactly like B01/B02/B06/B08 (ink outlines, cel colours, soft light), slightly desaturated so the white character pops in front.

## STEP 1: CHARACTER POSES (green #00FF00, full body unless stated, front view unless stated)
- C01 standing, arms crossed, confident (MAIN reference pose)
- C02 shrugging, both palms up
- C03 index finger raised up next to head ("listen / number one")
- C04 thinking: one hand on chin, other arm across the body
- C05 double-biceps flex
- C06 standing side-on (profile facing left), hands on hips, shoulders dropped (looking at himself in a mirror)
- C07 lying on a flat gym bench doing a bench press with a loaded barbell held up, 3/4 view (bench and barbell included in the image)
- C08 drinking from a protein shaker bottle with one hand, other hand on hip
- C09 sleeping peacefully lying on his back, seen from slightly above, hands resting on belly, eyes = the closed version of the black ovals (rule 7) (NO bed in the image, the editor places him on the bed plate)
- C10 exhausted sleep-deprived: slouching, arms hanging, head drooping, the same black oval eyes (rule 7), shown tired only by posture
- C11 shocked: both hands on the sides of the head
- C12 thumbs up
- C13 lying on his side curled up, holding a glowing smartphone close to his face in the dark (blue screen glow on his face), same black oval eyes (NO bed in the image)
- C14 one palm pushed forward toward the viewer ("stop" gesture), other hand holding a smartphone away behind him
- C15 holding a coffee cup in one hand and refusing it with the other hand making an X / waving no
- C16 carrying a tall stack of red bricks in both arms, walking to the right
- C17 the SAME character visibly LESS muscular: thinner arms, soft flat chest, small belly, slumped sad posture (muscle loss version), standing front view
- C18 holding up two fingers (V / number two)
- C19 holding up three fingers (number three)
- C20 sitting on the edge of (invisible) bed stretching both arms up (NO bed in the image)
- C21 half-body close-up (waist up) pointing straight at the viewer
- C22 half-body close-up (chest up) of the face looking straight at the viewer, serious
- C23 sneaking pose: tiptoeing to the right, carrying a hammer (the "thief who tears down the wall at night")

## STEP 2: PROPS (green #00FF00, one object each, 3/4 view)
- R01 protein shaker bottle (blank label)
- R02 loaded barbell, horizontal
- R03 soft white pillow
- R04 healthy red muscle fiber bundle (stylised anatomy, like a red striped spindle)
- R05 the same muscle fiber bundle but with small tears and cracks (damaged after training)
- R06 glowing teal growth-hormone molecule / small capsule with sparkles (healing energy)
- R07 small yellow fat cell blob (soft round droplet with a cute bubbly texture)
- R08 crescent moon with two small stars
- R09 classic twin-bell alarm clock (blank face, only hands)
- R10 smartphone with glowing blue blank screen
- R11 coffee mug with steam
- R12 pile of supplement tubs and pill bottles (blank labels)
- R13 single red brick
- R14 small orange hard hat (construction worker helmet) lying on the ground
- R15 bathroom weight scale, top view slightly tilted
- R16 calendar page with a big blank square (no numbers)
- R17 research paper / scientific journal page with blank grey lines and a small bar chart (no readable text)
- R18 large white bed (single bed) seen from the same slightly-high front angle as B02, with pillow and plain light-grey blanket, as a separate cut-out (for layering the sleeping character between bed and blanket is NOT needed)

## STEP 3: BACKGROUND PLATES (16:9, empty, no characters, no green)
- B01 bright modern home gym corner: rubber floor, dumbbell rack on the left wall, a large window with daylight on the right, empty floor space in the centre-bottom for the character
- B02 cosy bedroom at NIGHT, slightly-high front view: a single bed in the centre with a pillow and a light blanket (empty bed), a bedside table with a warm small lamp, a window with blue moonlight, calm blue-teal mood
- B03 the same bedroom at night but dark and harsh: lamp off, only a cold blue phone-screen glow feeling, messy blanket, a wall clock (no numbers, hands at ~2 o'clock)
- B04 clean bathroom with a large wall mirror on the left half (the mirror shows only a soft blurred reflection of the tiles, no person), white tiles, morning light
- B05 university research lab / study room: whiteboard with simple blank charts, a desk with papers, soft daylight (no people)
- B06 construction site in DAYTIME: a half-built red-brick house wall in the centre, scaffolding, a pile of bricks on the left, blue sky
- B07 the SAME construction site at NIGHT: the brick wall is partly torn down with loose bricks on the ground, dark blue sky with moon, no workers
- B08 sunny kitchen in the afternoon: counter with a coffee machine, a wall clock (no numbers, hands at 2 o'clock), warm light
- B09 bedroom at early MORNING: same room style as B02, sunrise light through the window, blanket folded neatly, fresh bright mood

## CHECKLIST BEFORE YOU FINISH
- 23 character poses C01-C23 (green screen, same character everywhere: WHITE body, BLACK oval eyes, no mouth, black wristbands, charcoal shorts)
- 18 props R01-R18 (green screen)
- 9 background plates B01-B09 (16:9, empty)
Total: 50 images, named by ID. EYES rule 7 respected in every character image, backgrounds in the same cartoon style. If any character has a mouth, a nose, eyes that are not the two identical black ovals of EYE-REF.png, or a background that is not in the B01/B02 cartoon style, redo that item.
