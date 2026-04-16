CHALLENGES = [
    {
        "id": 1,
        "title": "Rule of Thirds",
        "category": "Composition",
        "difficulty": "Beginner",
        "emoji": "📐",
        "xp": 50,
        "description": (
            "Capture any subject using the rule of thirds. "
            "Place your main subject at one of the four grid intersection points — "
            "not in the centre of the frame."
        ),
        "requirements": [
            "Subject is positioned at or near a thirds intersection point",
            "Subject is NOT centred in the frame",
            "Background occupies at least one third of the image",
        ],
        "tip": "Enable the grid overlay in your camera app. The intersections are your power spots.",
        "eval_context": "Check if the main subject is offset from centre and placed near a thirds grid line or intersection.",
    },
    {
        "id": 2,
        "title": "Golden Hour Glow",
        "category": "Lighting",
        "difficulty": "Beginner",
        "emoji": "🌅",
        "xp": 75,
        "description": (
            "Shoot a portrait or landscape during golden hour — "
            "within 60 minutes of sunrise or sunset. "
            "Use the warm directional light to create depth and warmth."
        ),
        "requirements": [
            "Warm golden or orange tones are clearly visible",
            "Directional side or backlight from the sun is present",
            "Soft shadows and minimal harsh contrast on the subject",
        ],
        "tip": "Stand with the sun behind or to the side of your subject for a beautiful rim-light glow.",
        "eval_context": "Look for warm colour temperature, soft directional light, and golden tones typical of sunrise/sunset.",
    },
    {
        "id": 3,
        "title": "Bokeh Master",
        "category": "Camera Technique",
        "difficulty": "Beginner",
        "emoji": "🌸",
        "xp": 75,
        "description": (
            "Create a photo with a sharp subject and a creamy blurred background. "
            "Use portrait mode on your phone or a wide aperture on a camera."
        ),
        "requirements": [
            "Main subject is sharp and in crisp focus",
            "Background is visibly blurred (bokeh effect)",
            "Clear visual separation between subject and background",
        ],
        "tip": "On a phone use Portrait mode. On a camera, set the lowest f-number available and get close to your subject.",
        "eval_context": "Evaluate the sharpness of the subject vs the blur level of the background. Is there clear depth separation?",
    },
    {
        "id": 4,
        "title": "Leading Lines",
        "category": "Composition",
        "difficulty": "Intermediate",
        "emoji": "🛤️",
        "xp": 100,
        "description": (
            "Use natural or man-made lines in the scene to guide the viewer's eye "
            "toward your subject or through the frame. Roads, fences, rivers, and "
            "corridors all work great."
        ),
        "requirements": [
            "At least one strong leading line is visible",
            "The line directs the eye toward a subject or vanishing point",
            "The composition creates a sense of depth or journey",
        ],
        "tip": "Get low to the ground — it exaggerates perspective and makes lines more dramatic.",
        "eval_context": "Identify leading lines in the image. Do they guide the viewer's eye toward a point of interest?",
    },
    {
        "id": 5,
        "title": "Freeze the Action",
        "category": "Camera Technique",
        "difficulty": "Intermediate",
        "emoji": "⚡",
        "xp": 125,
        "description": (
            "Capture a fast-moving subject completely frozen in time — "
            "no motion blur on the subject. Think sports, water splash, "
            "a pet mid-jump, or someone throwing an object."
        ),
        "requirements": [
            "The moving subject is sharp with no motion blur",
            "The action or movement is clearly visible",
            "The subject is well-exposed and not underexposed",
        ],
        "tip": "Use Shutter Priority (Tv/S) mode. Set shutter speed to 1/500s or faster. Shoot outdoors in bright light.",
        "eval_context": "Is the subject frozen and sharp? Is there evidence of fast motion in the scene (action, sport, splash)?",
    },
    {
        "id": 6,
        "title": "Rembrandt Lighting",
        "category": "Lighting",
        "difficulty": "Intermediate",
        "emoji": "🎭",
        "xp": 125,
        "description": (
            "Recreate the classic Rembrandt lighting pattern on a portrait. "
            "The subject should have shadow on one side of the face with a "
            "small triangle of light on the shadowed cheek."
        ),
        "requirements": [
            "One side of the face is clearly in shadow",
            "A small triangle of light is visible on the shadow-side cheek",
            "Dramatic contrast between lit and shadowed sides of the face",
        ],
        "tip": "Place a window or lamp at roughly 45° above and to the side of your subject. Adjust until you see the triangle.",
        "eval_context": "Look for the classic Rembrandt triangle — a small patch of light on the darker cheek. Is the lighting ratio dramatic?",
    },
    {
        "id": 7,
        "title": "Silhouette Drama",
        "category": "Lighting",
        "difficulty": "Intermediate",
        "emoji": "🌇",
        "xp": 100,
        "description": (
            "Create a dramatic silhouette photo. Your subject must appear "
            "completely dark against a bright background. Sunsets, windows, "
            "and open doorways work perfectly."
        ),
        "requirements": [
            "Subject is a solid dark silhouette with no visible detail",
            "Background is bright and well-exposed",
            "Subject's outline/shape is clean and instantly recognisable",
        ],
        "tip": "Expose for the bright background. Tap the bright area on your phone screen to set exposure there.",
        "eval_context": "Is the subject a true silhouette (dark, no detail)? Is the background bright and colourful? Is the outline recognisable?",
    },
    {
        "id": 8,
        "title": "Frame Within a Frame",
        "category": "Composition",
        "difficulty": "Intermediate",
        "emoji": "🖼️",
        "xp": 100,
        "description": (
            "Use an element in the scene — a doorway, window, arch, tunnel, "
            "or overhanging branches — to frame your subject inside the shot."
        ),
        "requirements": [
            "A secondary frame element (arch, window, doorway, etc.) is visible",
            "The main subject is positioned inside or visible through the frame",
            "The framing element adds depth and draws attention to the subject",
        ],
        "tip": "Arches, tunnels, windows, and even dense foliage make great natural frames.",
        "eval_context": "Is there a clear framing element that creates a frame-within-a-frame composition? Does it direct attention to the subject?",
    },
    {
        "id": 9,
        "title": "Long Exposure Light Trails",
        "category": "Camera Technique",
        "difficulty": "Advanced",
        "emoji": "🌃",
        "xp": 200,
        "description": (
            "Capture light trails from moving cars or any light source "
            "using a long exposure. A tripod is essential. "
            "Best done at dusk or night on a busy road."
        ),
        "requirements": [
            "Visible smooth light trails from moving light sources",
            "Background and static elements are sharp (no camera shake)",
            "Exposure is clearly several seconds long",
        ],
        "tip": "Use Bulb or Manual mode. Set shutter to 5–30 seconds, ISO 100, f/8. A tripod is non-negotiable.",
        "eval_context": "Are there smooth light trails? Is the static background sharp? Does the image convey a long exposure?",
    },
    {
        "id": 10,
        "title": "Reflection Symmetry",
        "category": "Composition",
        "difficulty": "Advanced",
        "emoji": "🪞",
        "xp": 150,
        "description": (
            "Find a reflective surface — puddle, lake, glass building, mirror — "
            "and create a symmetrical or near-symmetrical composition "
            "using the reflection."
        ),
        "requirements": [
            "A clear reflection is prominently visible in the image",
            "The composition uses the reflection as a key visual element",
            "The reflection adds symmetry, depth, or a surreal quality",
        ],
        "tip": "Puddles after rain are perfect. Get low and shoot at a very shallow angle for a clean reflection.",
        "eval_context": "Is there a clear reflection in the image? Does it contribute meaningfully to the composition and create symmetry or depth?",
    },
]

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
DIFFICULTY_COLOR = {
    "Beginner": "#4caf50",
    "Intermediate": "#f0a500",
    "Advanced": "#e74c3c",
}
