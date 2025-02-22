# colors.py

from enum import Enum

class Colors(str, Enum):
    # ─────────────────────────────────────────────
    # 1) Red(빨강) 계열 42가지
    # ─────────────────────────────────────────────
    Red001 = "기본빨강"
    Red002 = "밝은빨강"
    Red003 = "어두운빨강"
    Red004 = "연빨강"
    Red005 = "진빨강"
    Red006 = "선홍빨강"
    Red007 = "토마토빨강"
    Red008 = "체리빨강"
    Red009 = "딸기빨강"
    Red010 = "루비빨강"
    Red011 = "로즈빨강"
    Red012 = "버건디빨강"
    Red013 = "석류빨강"
    Red014 = "장밋빛빨강"
    Red015 = "코랄빨강"
    Red016 = "산호빨강"
    Red017 = "스칼렛빨강"
    Red018 = "크림슨빨강"
    Red019 = "파스텔빨강"
    Red020 = "네온빨강"
    Red021 = "메탈릭빨강"
    Red022 = "펄빨강"
    Red023 = "홀로그램빨강"
    Red024 = "폴리쉬빨강"
    Red025 = "가넷빨강"
    Red026 = "사과빨강"
    Red027 = "플라밍고빨강"
    Red028 = "홍차빨강"
    Red029 = "샤이니빨강"
    Red030 = "글로시빨강"
    Red031 = "마르살라빨강"
    Red032 = "와인빨강"
    Red033 = "브릭레드"
    Red034 = "피망빨강"
    Red035 = "레드페퍼"
    Red036 = "칼라베리빨강"
    Red037 = "레드벨벳"
    Red038 = "페일레드"
    Red039 = "라즈베리빨강"
    Red040 = "크랜베리빨강"
    Red041 = "딥체리빨강"
    Red042 = "플럼레드"

    # ─────────────────────────────────────────────
    # 2) Orange(주황) 계열 42가지
    # ─────────────────────────────────────────────
    Orange001 = "기본주황"
    Orange002 = "밝은주황"
    Orange003 = "어두운주황"
    Orange004 = "연주황"
    Orange005 = "진주황"
    Orange006 = "만다린오렌지"
    Orange007 = "호박주황"
    Orange008 = "브릭오렌지"
    Orange009 = "파스텔오렌지"
    Orange010 = "네온오렌지"
    Orange011 = "메탈릭오렌지"
    Orange012 = "펄오렌지"
    Orange013 = "샤이니오렌지"
    Orange014 = "글로시오렌지"
    Orange015 = "코랄오렌지"
    Orange016 = "캐러멜오렌지"
    Orange017 = "살구주황"
    Orange018 = "피치주황"
    Orange019 = "다홍주황"
    Orange020 = "새먼오렌지"
    Orange021 = "황토주황"
    Orange022 = "골든오렌지"
    Orange023 = "쿠퍼오렌지"
    Orange024 = "파파야주황"
    Orange025 = "앙버오렌지"
    Orange026 = "에너지오렌지"
    Orange027 = "카렌듈라오렌지"
    Orange028 = "선셋오렌지"
    Orange029 = "코랄핑크빛주황"
    Orange030 = "소프트오렌지"
    Orange031 = "머스크멜론오렌지"
    Orange032 = "샤벳오렌지"
    Orange033 = "마멀레이드오렌지"
    Orange034 = "클리멘타인오렌지"
    Orange035 = "아프리콧오렌지"
    Orange036 = "트로피컬오렌지"
    Orange037 = "로브스터오렌지"
    Orange038 = "블러드오렌지"
    Orange039 = "이그나이트오렌지"
    Orange040 = "쥬시오렌지"
    Orange041 = "태양오렌지"
    Orange042 = "플레임오렌지"

    # ─────────────────────────────────────────────
    # 3) Yellow(노랑) 계열 42가지
    # ─────────────────────────────────────────────
    Yellow001 = "기본노랑"
    Yellow002 = "밝은노랑"
    Yellow003 = "어두운노랑"
    Yellow004 = "연노랑"
    Yellow005 = "진노랑"
    Yellow006 = "샛노랑"
    Yellow007 = "카나리아노랑"
    Yellow008 = "밀짚노랑"
    Yellow009 = "파스텔노랑"
    Yellow010 = "네온노랑"
    Yellow011 = "메탈릭노랑"
    Yellow012 = "펄노랑"
    Yellow013 = "레몬노랑"
    Yellow014 = "머스터드노랑"
    Yellow015 = "골든옐로우"
    Yellow016 = "버터노랑"
    Yellow017 = "아몬드노랑"
    Yellow018 = "크림노랑"
    Yellow019 = "아이보리노랑"
    Yellow020 = "베이지노랑"
    Yellow021 = "라이트골드"
    Yellow022 = "딥골드"
    Yellow023 = "하이라이터옐로우"
    Yellow024 = "브라이트옐로우"
    Yellow025 = "스포트라이트옐로우"
    Yellow026 = "소프트옐로우"
    Yellow027 = "코ーン옐로우"
    Yellow028 = "맥앤치즈옐로우"
    Yellow029 = "선샤인옐로우"
    Yellow030 = "라이트머스터드"
    Yellow031 = "골든로드"
    Yellow032 = "망고옐로우"
    Yellow033 = "바나나옐로우"
    Yellow034 = "포슬린옐로우"
    Yellow035 = "하니머스타드"
    Yellow036 = "라이트카레옐로우"
    Yellow037 = "피나콜라다옐로우"
    Yellow038 = "밀키옐로우"
    Yellow039 = "코스믹옐로우"
    Yellow040 = "폴리쉬옐로우"
    Yellow041 = "올드골드"
    Yellow042 = "선플라워옐로우"

    # ─────────────────────────────────────────────
    # 4) Green(초록/연두/청록) 계열 42가지
    # ─────────────────────────────────────────────
    Green001 = "기본초록"
    Green002 = "밝은초록"
    Green003 = "어두운초록"
    Green004 = "연초록"
    Green005 = "진초록"
    Green006 = "라임초록"
    Green007 = "애플그린"
    Green008 = "민트초록"
    Green009 = "연두색"
    Green010 = "진연두색"
    Green011 = "파스텔초록"
    Green012 = "네온초록"
    Green013 = "메탈릭초록"
    Green014 = "펄초록"
    Green015 = "포레스트그린"
    Green016 = "올리브그린"
    Green017 = "에메랄드그린"
    Green018 = "비취색"
    Green019 = "삼림초록"
    Green020 = "시트러스그린"
    Green021 = "청사과색"
    Green022 = "브로콜리그린"
    Green023 = "키위그린"
    Green024 = "아보카도그린"
    Green025 = "카키그린"
    Green026 = "세이지그린"
    Green027 = "피스타치오그린"
    Green028 = "터콰이즈(청록)"
    Green029 = "진청록"
    Green030 = "파스텔청록"
    Green031 = "네온청록"
    Green032 = "티파니그린"
    Green033 = "스프링그린"
    Green034 = "파라다이스그린"
    Green035 = "펀치그린"
    Green036 = "몰디브그린"
    Green037 = "아쿠아그린"
    Green038 = "프로스트그린"
    Green039 = "샤이니그린"
    Green040 = "글로시그린"
    Green041 = "라이트올리브"
    Green042 = "딥라임그린"

    # ─────────────────────────────────────────────
    # 5) Blue(파랑/남색) 계열 42가지
    # ─────────────────────────────────────────────
    Blue001 = "기본파랑"
    Blue002 = "밝은파랑"
    Blue003 = "어두운파랑"
    Blue004 = "연파랑"
    Blue005 = "진파랑"
    Blue006 = "파스텔파랑"
    Blue007 = "네온파랑"
    Blue008 = "메탈릭파랑"
    Blue009 = "펄파랑"
    Blue010 = "하늘색"
    Blue011 = "스카이블루"
    Blue012 = "네이비블루"
    Blue013 = "코발트블루"
    Blue014 = "로열블루"
    Blue015 = "미드나잇블루"
    Blue016 = "오션블루"
    Blue017 = "마린블루"
    Blue018 = "애틀랜틱블루"
    Blue019 = "라이트블루"
    Blue020 = "딥블루"
    Blue021 = "인디고블루"
    Blue022 = "세룰리언블루"
    Blue023 = "데님블루"
    Blue024 = "아이스블루"
    Blue025 = "티파니블루"
    Blue026 = "그레이블루"
    Blue027 = "블루그린"
    Blue028 = "블루퍼플"
    Blue029 = "차가운블루"
    Blue030 = "아이리스블루"
    Blue031 = "폴라블루"
    Blue032 = "라군블루"
    Blue033 = "사파이어블루"
    Blue034 = "에어블루"
    Blue035 = "보석블루"
    Blue036 = "아쿠아블루"
    Blue037 = "퍼스트블루"
    Blue038 = "샤이니블루"
    Blue039 = "글로시블루"
    Blue040 = "딥네이비"
    Blue041 = "울트라마린블루"
    Blue042 = "베릴블루"

    # ─────────────────────────────────────────────
    # 6) Purple(보라/자주) 계열 42가지
    # ─────────────────────────────────────────────
    Purple001 = "기본보라"
    Purple002 = "밝은보라"
    Purple003 = "어두운보라"
    Purple004 = "연보라"
    Purple005 = "진보라"
    Purple006 = "라벤더보라"
    Purple007 = "퍼플"
    Purple008 = "바이올렛"
    Purple009 = "마젠타보라"
    Purple010 = "자주보라"
    Purple011 = "딥퍼플"
    Purple012 = "플럼보라"
    Purple013 = "파스텔보라"
    Purple014 = "네온보라"
    Purple015 = "메탈릭보라"
    Purple016 = "펄보라"
    Purple017 = "샤이니보라"
    Purple018 = "글로시보라"
    Purple019 = "오키드보라"
    Purple020 = "라일락보라"
    Purple021 = "포도보라"
    Purple022 = "스모키보라"
    Purple023 = "그레이쉬보라"
    Purple024 = "화이트퍼플"
    Purple025 = "라벤더그레이"
    Purple026 = "라일락그레이"
    Purple027 = "플루메리아보라"
    Purple028 = "엔드보라"
    Purple029 = "그레이핑크보라"
    Purple030 = "찬보라"
    Purple031 = "딥바이올렛"
    Purple032 = "딤퍼플"
    Purple033 = "스윗퍼플"
    Purple034 = "아메시스트보라"
    Purple035 = "울트라바이올렛"
    Purple036 = "드림퍼플"
    Purple037 = "루핀보라"
    Purple038 = "프로스트퍼플"
    Purple039 = "페어리보라"
    Purple040 = "피그보라"
    Purple041 = "네온라일락"
    Purple042 = "퍼플레인"

    # ─────────────────────────────────────────────
    # 7) Pink(분홍) 계열 42가지
    # ─────────────────────────────────────────────
    Pink001 = "기본분홍"
    Pink002 = "밝은분홍"
    Pink003 = "어두운분홍"
    Pink004 = "연분홍"
    Pink005 = "진분홍"
    Pink006 = "파스텔분홍"
    Pink007 = "네온분홍"
    Pink008 = "메탈릭분홍"
    Pink009 = "펄분홍"
    Pink010 = "핫핑크"
    Pink011 = "베이비핑크"
    Pink012 = "로즈핑크"
    Pink013 = "코랄핑크"
    Pink014 = "샤벳핑크"
    Pink015 = "플라밍고핑크"
    Pink016 = "새먼핑크"
    Pink017 = "캔디핑크"
    Pink018 = "수박핑크"
    Pink019 = "샤이니핑크"
    Pink020 = "글로시핑크"
    Pink021 = "체리블라썸핑크"
    Pink022 = "스모키핑크"
    Pink023 = "차분한핑크"
    Pink024 = "페일핑크"
    Pink025 = "티핑크"
    Pink026 = "말린장미핑크"
    Pink027 = "폼폼핑크"
    Pink028 = "버블검핑크"
    Pink029 = "라이트핑크"
    Pink030 = "핑크샴페인"
    Pink031 = "네온로즈핑크"
    Pink032 = "쉬머핑크"
    Pink033 = "프림로즈핑크"
    Pink034 = "딸기우유핑크"
    Pink035 = "아기볼핑크"
    Pink036 = "복숭아핑크"
    Pink037 = "로맨틱핑크"
    Pink038 = "프린세스핑크"
    Pink039 = "소프트핑크"
    Pink040 = "루미너스핑크"
    Pink041 = "호이얀핑크"  # 뜨는 관광지 '호이안'에서 영감 얻은 예시
    Pink042 = "러블리샤벳핑크"

    # ─────────────────────────────────────────────
    # 8) Brown/Beige(갈색·베이지) 계열 42가지
    # ─────────────────────────────────────────────
    Brown001 = "기본갈색"
    Brown002 = "밝은갈색"
    Brown003 = "어두운갈색"
    Brown004 = "연갈색"
    Brown005 = "진갈색"
    Brown006 = "마호가니갈색"
    Brown007 = "초콜릿갈색"
    Brown008 = "코코아갈색"
    Brown009 = "모카색"
    Brown010 = "밤색"
    Brown011 = "카푸치노색"
    Brown012 = "커피색"
    Brown013 = "테라코타색"
    Brown014 = "로즈골드브라운"
    Brown015 = "브론즈브라운"
    Brown016 = "샌드브라운"
    Brown017 = "카멜갈색"
    Brown018 = "위스키갈색"
    Brown019 = "가죽갈색"
    Brown020 = "오크브라운"
    Brown021 = "코르크브라운"
    Brown022 = "벽돌갈색"
    Brown023 = "고동색"
    Brown024 = "황토색"
    Brown025 = "새우갈색"
    Brown026 = "호두갈색"
    Brown027 = "진한커피색"
    Brown028 = "모카라떼색"
    Brown029 = "피넛브라운"
    Brown030 = "에스프레소갈색"
    Brown031 = "캐러멜갈색"
    Brown032 = "머쉬룸브라운"
    Brown033 = "파스텔브라운"
    Brown034 = "샌디베이지"
    Brown035 = "진베이지"
    Brown036 = "연베이지"
    Brown037 = "토피갈색"
    Brown038 = "스모키브라운"
    Brown039 = "그레이지브라운"
    Brown040 = "라떼브라운"
    Brown041 = "우드브라운"
    Brown042 = "포슬린베이지"

    # ─────────────────────────────────────────────
    # 9) Gray(회색) 계열 42가지
    # ─────────────────────────────────────────────
    Gray001 = "기본회색"
    Gray002 = "밝은회색"
    Gray003 = "어두운회색"
    Gray004 = "연회색"
    Gray005 = "진회색"
    Gray006 = "스모키그레이"
    Gray007 = "차콜그레이"
    Gray008 = "실버그레이"
    Gray009 = "메탈릭그레이"
    Gray010 = "펄그레이"
    Gray011 = "그레이지"
    Gray012 = "블루그레이"
    Gray013 = "라이트블루그레이"
    Gray014 = "딥블루그레이"
    Gray015 = "퍼플그레이"
    Gray016 = "핑크그레이"
    Gray017 = "브라운그레이"
    Gray018 = "그래파이트그레이"
    Gray019 = "아이언그레이"
    Gray020 = "스틸그레이"
    Gray021 = "웨더그레이"
    Gray022 = "미스트그레이"
    Gray023 = "스톤그레이"
    Gray024 = "우드애쉬그레이"
    Gray025 = "글로시그레이"
    Gray026 = "라일락그레이"
    Gray027 = "로즈그레이"
    Gray028 = "네온그레이"  # 실제론 어색
    Gray029 = "실버블루그레이"
    Gray030 = "라이트실버그레이"
    Gray031 = "다크실버그레이"
    Gray032 = "코스믹그레이"
    Gray033 = "티타늄그레이"
    Gray034 = "모카그레이"
    Gray035 = "도브그레이"
    Gray036 = "샤이니그레이"
    Gray037 = "프리즘그레이"
    Gray038 = "콘크리트그레이"
    Gray039 = "소프트그레이"
    Gray040 = "피존그레이"
    Gray041 = "라이트차콜그레이"
    Gray042 = "울트라그레이"

    # ─────────────────────────────────────────────
    # 10) Black(검정) 계열 42가지
    # ─────────────────────────────────────────────
    Black001 = "기본검정"
    Black002 = "밝은검정"
    Black003 = "어두운검정"
    Black004 = "연검정"
    Black005 = "진검정"
    Black006 = "차콜블랙"
    Black007 = "피치블랙"
    Black008 = "메탈릭블랙"
    Black009 = "펄블랙"
    Black010 = "유광블랙"
    Black011 = "무광블랙"
    Black012 = "샤이니블랙"
    Black013 = "스모키블랙"
    Black014 = "올블랙"
    Black015 = "딥블랙"
    Black016 = "잉크블랙"
    Black017 = "나이트블랙"
    Black018 = "에보니블랙"
    Black019 = "오닉스블랙"
    Black020 = "젯블랙"
    Black021 = "바이닐블랙"
    Black022 = "아이언블랙"
    Black023 = "라이트블랙"  # 회색 느낌
    Black024 = "블루블랙"
    Black025 = "퍼플블랙"
    Black026 = "레드블랙"
    Black027 = "브라운블랙"
    Black028 = "그린블랙"
    Black029 = "네온블랙"
    Black030 = "럭셔리블랙"
    Black031 = "다크차콜블랙"
    Black032 = "초콜릿블랙"  # 갈색 끼
    Black033 = "오팔블랙"
    Black034 = "미드나잇블랙"
    Black035 = "라이트차콜블랙"
    Black036 = "글로시블랙"
    Black037 = "실키블랙"
    Black038 = "피아노블랙"
    Black039 = "벨벳블랙"
    Black040 = "울트라블랙"
    Black041 = "매트블랙"
    Black042 = "크리스탈블랙"

    # ─────────────────────────────────────────────
    # 11) White(흰) 계열 42가지
    # ─────────────────────────────────────────────
    White001 = "기본흰색"
    White002 = "밝은흰색"
    White003 = "어두운흰색"
    White004 = "연흰색"
    White005 = "진흰색"
    White006 = "아이보리"
    White007 = "크림색"
    White008 = "베이지화이트"
    White009 = "펄화이트"
    White010 = "실버화이트"
    White011 = "샤이니화이트"
    White012 = "글로시화이트"
    White013 = "스모키화이트"
    White014 = "코튼화이트"
    White015 = "스노우화이트"
    White016 = "화이트골드"
    White017 = "화이트실버"
    White018 = "라이트화이트"
    White019 = "오프화이트"
    White020 = "앨러배스터화이트"
    White021 = "폴라화이트"
    White022 = "플래티넘화이트"
    White023 = "에그쉘화이트"
    White024 = "밀키화이트"
    White025 = "샌드화이트"
    White026 = "크림아이보리"
    White027 = "스톤화이트"
    White028 = "차분한화이트"
    White029 = "세라믹화이트"
    White030 = "치즈화이트"
    White031 = "트랜퀼화이트"
    White032 = "파스텔화이트"
    White033 = "루미너스화이트"
    White034 = "펄아이보리"
    White035 = "위스퍼화이트"
    White036 = "포슬린화이트"
    White037 = "폰드화이트"
    White038 = "클라우드화이트"
    White039 = "블루쉬화이트"
    White040 = "라이트그레이화이트"
    White041 = "다이아몬드화이트"
    White042 = "버터화이트"

    # ─────────────────────────────────────────────
    # 12) Special(특수) 계열 42가지
    # ─────────────────────────────────────────────
    Special001 = "레인보우(무지개)"
    Special002 = "오팔색"
    Special003 = "오로라색"
    Special004 = "홀로그램색"
    Special005 = "그라데이션"
    Special006 = "투명색"
    Special007 = "메탈릭골드"
    Special008 = "메탈릭실버"
    Special009 = "로즈골드"
    Special010 = "샴페인골드"
    Special011 = "플래티넘"
    Special012 = "티타늄실버"
    Special013 = "브론즈"
    Special014 = "구리색(코퍼)"
    Special015 = "진주색(펄)"
    Special016 = "크롬색"
    Special017 = "프로스트색"
    Special018 = "마블화이트"
    Special019 = "마블블랙"
    Special020 = "마블그레이"
    Special021 = "크리스탈색"
    Special022 = "글리터골드"
    Special023 = "글리터실버"
    Special024 = "스파클핑크"
    Special025 = "스파클블루"
    Special026 = "오일슬릭(오일필름)"
    Special027 = "나노코팅컬러"
    Special028 = "미러실버"
    Special029 = "버터플라이윙색"
    Special030 = "스노우글로브색"
    Special031 = "뉴이어스파클"
    Special032 = "은하수색"
    Special033 = "우주먼지색"
    Special034 = "파이어웍스색"
    Special035 = "하이퍼라이트색"
    Special036 = "판타지글로우"
    Special037 = "크로마틱실버"
    Special038 = "플래시골드"
    Special039 = "마더오브펄"
    Special040 = "캐러멜펄"
    Special041 = "무중력오로라"
    Special042 = "드래곤스케일"