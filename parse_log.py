import re, json
from collections import Counter

with open(r'c:\Users\rohai\Downloads\finished log 2020 to 2026-11-17.txt', encoding='utf-8-sig') as f:
    raw_lines = [l.strip() for l in f]

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_num = {m: str(i+1).zfill(2) for i, m in enumerate(months)}
date_pattern = re.compile(r'^(' + '|'.join(months) + r')\s+(\d{4}),\s*([A-Za-z]{3})$')
day_pattern = re.compile(r'^\d{1,2}$')

emoji_type = {
    '🎮': 'Game',
    '📺': 'TV Show',
    '🎬': 'Movie',
    '📖': 'Book',
    '📱': 'Comic',
    '🍿': 'Movie',
    '🎧': 'Audiobook',
    '🤖': 'Book',
}

TV_SHOW_TITLES = {
    'the boys', 'mob psycho 100 ii', 'star trek: discovery', 'parks and recreation',
    'cells at work!', 'defending jacob', 'the promised neverland',
    'fate/stay night: unlimited blade works', 'ford v ferrari', 'new girl',
    'modern family', 'the god of high school', 'orange', 'deca-dence', 'haikyu!',
    'haikyu!! to the top', 'higurashi', 'higurashi: kai', 'made in abyss',
    'wandavision', "queen's gambit", 'higurashi: when they cry – gou', 'vinland saga',
    'jujutsu kaisen', 'mushoku tensei: jobless reincarnation part 1', 'one-punch man',
    'redo of healer', 'the way of the househusband', 'the falcon and the winter soldier',
    "one-punch man ova's", 'life in pieces', "steins;gate 0", 'love, death & robots: volume 2',
    'fruits basket: the final', 'solos', 'loki', 'dr. stone', 'yu-gi-oh! duel monsters',
    'brooklyn nine-nine', 'nine perfect strangers', 'higurashi: when they cry – sotsu',
    'wandavision', 'tokyo revengers', 'the way of the househusband part 2',
    'the book of boba fett', 'mare of easttown', 'mushoku tensei: jobless reincarnation part 2',
    'jujutsu kaisen again', 'star wars: visions', 'peacemaker', 'obi-wan kenobi',
    'star trek: strange new worlds', 'spy × family (part 1)', 'the legend of vox machina',
    'under the banner of heaven', 'tower of god', 'ranking of kings', 'over the garden wall',
    'cyberpunk: edgerunners', "she-hulk: attorney at law", 'the lord of the rings: the rings of power',
    'tulsa king', 'house of the dragon', 'summer time rendering', 'the eminence in shadow',
    "anne rice's mayfair witches (2023)", 'odd taxi', 'uncle from another world',
    'the magical revolution of the reincarnated princess and the genius young lady',
    'farming life in another world', "chillin' in my 30s after getting fired from the demon king's army",
    'handyman saitou in another world', 'blue lock', 'campfire cooking in another world with my absurd skill',
    'the reincarnation of the strongest exorcist in another world', 'arknights: prelude to dawn',
    'tengoku daimakyo', 'oshi no ko', 'ahsoka', 'atelier ryza: ever darkness & the secret hideout the animation',
    'the walking dead: daryl dixon',
}

GAME_TITLES = {
    'star wars jedi: fallen order', 'mortal kombat 11', 'mortal kombat 11: aftermath',
    'batman: the enemy within', 'control (video game)', 'the last of us part ii',
    'the dark pictures anthology: man of medan', 'gotham knights (pc)', 'the evil within (pc)',
    'the evil within: the assignment', 'the evil within: the consequence', 'the evil within 2',
    'monster hunter freedom unite', 'fire emblem awakening', 'the callisto protocol',
    'lego marvel super heroes',
}

BOOK_TITLES = {
    'reading harry potter and the goblet of fire',
    'reading harry potter and the order of the phoenix',
    'harry potter and the half-blood prince',
    'reading harry potter and the deathly hallows',
}

COMIC_TITLES = {
    'marvel master reading order part 8', 'war of kings',
}

def infer_type_from_title(title):
    tl = title.lower()
    # Strip 'with Person' for matching
    tl_stripped = re.sub(r'\bwith\s+[A-Z][a-zA-Z].*$', '', tl).strip()

    if tl_stripped in TV_SHOW_TITLES or tl in TV_SHOW_TITLES:
        return 'TV Show'
    if tl_stripped in GAME_TITLES or tl in GAME_TITLES:
        return 'Game'
    if tl_stripped in BOOK_TITLES or tl in BOOK_TITLES:
        return 'Book'
    if tl_stripped in COMIC_TITLES or tl in COMIC_TITLES:
        return 'Comic'

    comic_kws = [' vol.', ' tp', ' hc', ' omnibus', 'graphic novel', 'trade paperback', 'hardcover']
    game_kws = [
        'resident evil', 'kingdom hearts', 'code vein', 'sekiro', 'uncharted',
        'death stranding', 'injustice', 'onimusha', 'pokemon', 'one piece: pirate',
        'new game plus', 'final fantasy', 'devil may cry', 'dark souls', 'bloodborne',
        'elden ring', 'god of war', 'spiderman', 'spider-man', 'batman: arkham',
        'horizon', 'ghost of tsushima', 'demon slayer: hinokami', 'judgment',
        'lost judgment', 'mortal kombat', 'star wars jedi', 'the evil within',
        'gotham knights', 'the callisto protocol', 'fire emblem', 'monster hunter',
        'control (video', 'batman: the enemy', 'lego marvel', 'the last of us',
        'dark pictures', 'atelier ryza'
    ]
    tv_kws = ['season', ' ep', '(finale)', 'arc', 'part 1', 'part 2', 'series']
    movie_kws = ['marathon', 'trilogy']

    for k in comic_kws:
        if k in tl:
            return 'Comic'
    for k in game_kws:
        if k in tl:
            return 'Game'
    for k in tv_kws:
        if k in tl:
            return 'TV Show'
    for k in movie_kws:
        if k in tl:
            return 'Movie'
    return 'TV Show'  # most untagged items are TV/anime

def parse_entry(title_raw):
    media_type = None
    for em, tp in emoji_type.items():
        if title_raw.startswith(em):
            media_type = tp
            title_raw = title_raw[len(em):].strip()
            break

    stars = title_raw.count('⭐')
    title_raw = title_raw.replace('⭐', '').strip()

    # Handle "Reading X with Y" -> Book
    reading_match = re.match(r'^Reading\s+(.+)$', title_raw, re.IGNORECASE)
    if reading_match and not media_type:
        media_type = 'Book'

    # Extract 'with Person(s)' - only at end or before a parenthetical
    # Support: "with Mazra", "with Mazra and Adeel", "with Mazra, Adeel and Aliza"
    with_match = re.search(r'\bwith\s+([A-Z][a-zA-Z]+(?:(?:\s*,\s*|\s+and\s+)[A-Z][a-zA-Z&]+)*(?:\s+and\s+[A-Z][a-zA-Z]+)?)\s*(?:\(|$)', title_raw)
    watched_with = None
    if with_match:
        watched_with = with_match.group(1).strip().rstrip(',').strip()

    # Remove 'Finished' or 'Fully Finished' prefix
    title = re.sub(r'^(Fully\s+)?Finished\s+', '', title_raw, flags=re.IGNORECASE).strip()
    # Remove 'Reading' prefix
    title = re.sub(r'^Reading\s+', '', title, flags=re.IGNORECASE).strip()

    if not media_type:
        media_type = infer_type_from_title(title)

    return {
        'title': title,
        'media_type': media_type,
        'rating': stars if stars > 0 else None,
        'watched_with': watched_with,
    }

current_day = None
current_month = None
current_year = None
current_dow = None
entries = []

i = 0
while i < len(raw_lines):
    line = raw_lines[i]
    if not line:
        i += 1
        continue
    if day_pattern.match(line) and i + 1 < len(raw_lines) and date_pattern.match(raw_lines[i+1]):
        current_day = int(line)
        m = date_pattern.match(raw_lines[i+1])
        current_month = m.group(1)
        current_year = int(m.group(2))
        current_dow = m.group(3)
        i += 2
        continue
    elif line == 'All day':
        i += 1
        continue
    else:
        if 'finish' in line.lower():
            parsed = parse_entry(line)
            parsed['date'] = f'{current_year}-{month_num[current_month]}-{str(current_day).zfill(2)}'
            parsed['year'] = current_year
            parsed['month'] = current_month
            parsed['month_num'] = int(month_num[current_month])
            parsed['day_of_week'] = current_dow
            entries.append(parsed)
        i += 1

print(f'Total entries: {len(entries)}')
type_dist = Counter(e['media_type'] for e in entries)
print('Type distribution:', dict(sorted(type_dist.items(), key=lambda x: -x[1])))
year_dist = Counter(e['year'] for e in entries)
print('Year distribution:', dict(sorted(year_dist.items())))
rated = [e for e in entries if e['rating']]
print(f'Entries with ratings: {len(rated)}')
ww = Counter(e['watched_with'] for e in entries if e['watched_with'])
print('Watched with (top 10):', dict(ww.most_common(10)))

with open(r'c:\Users\rohai\Downloads\AI\Shelfie\shelfie_data.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)
print('Saved shelfie_data.json')
