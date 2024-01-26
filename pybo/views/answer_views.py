from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
import numpy as np

lst = ["fuck","shit","18nom","18num","18ㅅㅐㄲㅣ","18ㅅㅐ끼","18ㅅㅔㅋㅣ","18ㅅㅔ키","18년","18놈","18새끼","18세ㅋㅣ","18세키","boji","bozi","dogbaby","d쥐고","d지고","jaji","jazi","jot같","me췬","me친","me틴","mi친","mi틴","sex하자","sex해","yadong","ya동","zaji","zazi","ㅁㅊ","ㅁㅣ췬","ㅁ친",
    "ㅂㄹ","ㅂㅁㄱ","ㅂㅊ","ㅂ크","ㅄ","ㅅ.ㅂ","ㅅㄲ네","ㅅㄲ들","ㅅㅂ","ㅅㅍ","ㅅㅋ","ㅅㅐㄲㅣ","ㅅㅡ루","ㅅ루","ㅅ발","ㅆㄹㄱ","ㅆㄺ","ㅆㅂ","ㅆㅣ","ㅆㅣ8","ㅆㅣㅂㅏ",
    "ㅆㅣ댕","ㅆㅣ뎅","ㅆㅣ바","ㅆㅣ발","ㅆㅣ팍넘","ㅇㅍㅊㅌ","ㅇㅒ쁜","ㅈ.ㄴ","ㅈㄴ","ㅈㄹ","ㅈㅏ위","ㅈ리","ㅉ질한","ㅌㅓㄹㅐㄱㅣ","凸","ㄱㅅㄲ","가슴만져","가슴빨아",
    "가슴빨어","가슴조물락","가슴주물럭","가슴쪼물딱","가슴쪼물락","가슴핧아","가슴핧어","강간","강간한다","같은새끼","개.웃","개가튼","개가튼년","개가튼뇬","개간","개같",
    "개같은년","개같이","개거얼래","개거얼레","개걸래","개걸레","개고치","개너미","개넷","개년","개념빠가","개놈","개독","개라슥","개련","개마이","개보지","개보지년",
    "개부달","개부랄","개불랄","개붕알","개새기","개새끼","개색뀌","개색휘","개샛기","개섹","개셈","개소리","개쉐뀌","개쓰래기","개쓰레기","개씁년","개씁블","개씁자지",
    "개씨발","개씨발넘","개씨발자슥","개씨블","개아기","개애거얼래","개애걸래","개에가튼","개에거얼래","개에걸래","개자식","개자지","개작두넘","개작두년","개잡년","개잡지랄",
    "개저가튼","개저씨","개저엇","개젓","개젓가튼넘","개좆","개지랄","개지랄넘","개지랄놈","개쩌","개후라","개후라년","개후라들놈","개후라새끼","걔잡년","걔잡지랄","거시기",
    "거지같은","걸래년","걸레같은년","걸레년","걸레보지","걸레핀년","게가튼","게부럴","게에가튼","게저엇","게젓","게지랄놈","계새끼","골빈","공알","괘새끼","괴가튼","괴에가튼?",
    "구씹","굿보지","귀두","그나물에","김대중","김치녀","꼭지","깨쌔끼","나빼썅","나쁜새끼","난자마셔","난자먹어","난자핧아","내꺼빨아","내꺼핧아","내미랄","내미럴","내버지",
    "내씨발","내자지","내잠지","내조지","너거애비","년놈","노네들","노무노무","노알라","노무현","뇌텅","뇨온","뇬","누나강간","느그매","늬믜","늬미","니기미","니년","니믜",
    "니미","니미기","니미랄","니미럴","니씨브랄","니아범","니아범?","니애미","니애비","니할애비","닝기리","닥쳐","닥쳐라","닥치세","달달이","달딸이","닳은년","대가리","대갈",
    "대애가리","대에가리","대음순","더어엉신","더엉신","더러운년","덜은새끼","돈년","돈새끼","돌았네","돌으년","돌은새끼","동생강간","뒈져","뒤이치기","뒤져라","뒤져버","뒤져야",
    "뒤져야지","뒤져요","뒤졌","뒤지겠","뒤지고싶","뒤지길","뒤진다","뒤질","뒤치기","뒷잇치기","뒷치기","드으응신","드응신","등신","디져라","디졌","디지고","디질","따먹기",
    "따먹는다","따먹어","따먹어야지","따먹었어","따먹었지","따먹을까","따먹자","따아알따리","따아알따아리","따알따리","딴년","딸달이","딸딸이","떠라이","떠어라아이","떠어라이",
    "또라이","또라인","또오라아이","또오라이","똘아이","띠바","띠발","띠발뇬","띠벌","띠벨","띠부우울","띠부울","띠불","띠브울","띠블","띠블넘","띠이바알","띠이발","띠이버얼",
    "띠이벌","띠이이발","띠이이벌","런년","럼들","롬들","막간년","막대쑤셔줘?","막대핧아줘","맘충","맛간년","맛없는년","맛이간년","머갈","믜칀","믜친","미띤","미시친발",
    "미쳣네","미쳤나","미쳤니","미췬","미칀","미치인","미친","미친ㅋ","미친개","미친구녕","미친구멍","미친넘","미친년","미친놈","미친눔","미친새","미친새끼","미친색","미친쉐이",
    "미친씨부랄","미티넘","미틴","미틴것","및힌","바주카자지","발놈","방점뱅","백보지","버따리자지","버어어지","버어어지이","버어지","버어지이","버지구녕","버지구멍","버지냄새",
    "버지따먹기","버지뚫어","버지뜨더","버지물마셔","버지벌려","버지벌료","버지빨아","버지빨어","버지썰어","버지쑤셔","버지털","버지핧아","버짓물","버짓물마셔","벌창","벌창같은년",
    "벵신","별창","병닥","병딱","병맛","병신","병신세리","병신셰리","병신씨발","병크","보지","보지구녕","보지구멍","보지녀","보지따먹기","보지뚫어","보지뜨더","보지머리박기",
    "보지물","보지물마셔","보지박어","보지벌려","보지벌료","보지벌리","보지벌리자","보지보지","보지빨아","보지빨어","보지에자지껴","보지에자지너","보지자지","보지정액","보지쥐어짜",
    "보지찌져","보지찢어","보지털","보지털뽑아","보지털어","보지틀래기","보지핧아","보지핧아줄까","보지핧아줘","보지핧어","보짓물","보짓물마셔","봉알","부랄","불알","붕신","붕알",
    "뷰우웅신","뷰웅시인","뷰웅신","븅신","브랄","빙띤","빙신","빙신쉐이","빠가야로","빠가냐","빠간가","빠가새","빠가니","빠가십새","빠가씹새","빠구리","빠구울","빠굴",
    "빠굴이","빠네","빠라","빠아가","빠아구리","빠아구우리","빠아아라","빠큐","빡새끼","빨치산","빻았","빻은","뻐규","뻐큐","뻑유","뻑큐","뻨큐","뼈큐","뽀지","사까쉬","사까시",
    "사까시이","사까아시","사까아시이","사새끼","상년","새77ㅣ","새ㄲㅣ","새끼","새끼라","새끼야","새퀴","새킈","새키","색희","색히","샊기","샊히","샹년","섀키","성괴","성교",
    "성교하자","성교해","성폭행","세끼","세엑스","세엑쓰","세키","섹끼","섹스","섹스하자","섹스해","소음순","쇅끼","쇡끼","쉐끼","쉬박","쉬발","쉬방새","쉬버","쉬빡","쉬이바",
    "쉬이이","쉬이이이","쉬이이이이","쉬탱","쉬팍","쉬펄","쉽세","쉽알넘","슈ㅣ발","슈발","슈벌","슈우벌","스벌","슨상님","싑창","시댕이","시미발친","시미친발","시바","시파",
    "시바라지","시바류","시바시바","시바알","시바앙","시박색히","시박쉑히","시발","시발년","시발놈","시발새끼","시방새","시방색희","시방쉑희","시벌","시벌탱","시볼탱","시부럴",
    "시부렬","시부울","시뷰럴","시뷰렬","시빡","시빨","시새발끼","시이발","시입세","시입세에","시친발미","시키가","시탱","시팍","시팍새끼","시팔","시팔넘","시팔년","시팔놈",
    "시팔새끼","시펄","십녀","십버지","십부랄","십부럴","십새","십세","십세리","십세이","십셰리","십쉐끼","십자석","십자슥","십지랄","십창","십창녀","십탱","십탱구리","십탱굴이",
    "십팔","십팔넘","십팔새끼","싸가지","싸가지없","싸물어","싹스","쌍년","쌍놈","쌍보지","쌍쌍보지","쌔끼","쌔엑스","쌕스","쌕쓰","썅","썅놈","썅년","썌끼","쎄끼","쎄리","쎄엑스",
    "쎅스","쎅쓰","쒸8","쒸댕","쒸발","쒸팔","쒸펄","쓰댕","쓰뎅","쓰래기같","쓰레기새","쓰렉","쓰루","쓰바","쓰바새끼","쓰발","쓰벌","쓰벨","쓰브랄쉽세","쓰파","씌8","씌댕","씌뎅",
    "씌발","씌벨","씌팔","씝창","씨8","씨ㅂㅏ","씨가랭넘","씨가랭년","씨가랭놈","씨걸","씨댕","씨댕이","씨뎅","씨바","씨바라","씨바알","씨박색희","씨박색히","씨박쉑히",
    "씨발","씨발년","씨발롬","씨발병신","씨방새","씨방세","씨뱅가리","씨버럼","씨벌","씨벌년","씨벌쉐이","씨벌탱","씨벨","씨볼탱","씨부랄","씨부럴","씨부렬","씨불알","씨뷰럴",
    "씨뷰렬","씨브럴","씨블","씨블년","씨븡","씨븡새끼","씨비","씨빠빠","씨빡","씨빨","씨뻘","씨새발끼","씨섹끼","씨이발","씨입","씨입새","씨입새에","씨입세","씨입세에","씨파넘",
    "씨팍","씨팍넘","씨팍새끼","씨팍세끼","씨팔","씨퐁","씨퐁넘","씨퐁뇬","씨퐁보지","씨퐁자지","씹","씹귀","씹년","씹덕","씹못","씹물","씹미랄","씹버지","씹보지","씹부랄","씹브랄",
    "씹빵구","씹뻐럴","씹뽀지","씹새","씹새끼","씹세","씹쉐뀌","씹쌔","씹쌔끼","씹자석","씹자슥","씹자지","씹지랄","씹창","씹창녀","씹치","씹탱","씹탱굴이","씹탱이","씹팔","씹팔넘",
    "씹할","아가리","아닥","아아가리","아오ㅅㅂ","아오시바","암캐년","애무","애미","애미랄","애미보지","애미씨뱅","애미자지","애미잡년","애미좃물","애비","애애무","애에무","애에미","애에비",
    "앰창","야dong","야동","어미강간","어미따먹자","어미쑤시자","엄창","에무","에미","에비","에애무","에에무","에에미","에에비","엠생","엠창","여어엄","여엄병","여자ㄸㅏ먹기","여자ㄸㅏ묵기",
    "여자따먹기","여자따묵기","염병","염병할","염뵹","엿같","엿먹어라","엿이나","옘병","오르가즘","왕버지","왕자지","왕잠지","왕털버지","왕털보지","왕털자지","왕털잠지","왜저럼","외퀴",
    "요년","유깝","유두","유두빨어","유두핧어","유발조물락","유방","유방만져","유방빨아","유방주물럭","유방쪼물딱","유방쪼물럭","유방핧아","유방핧어","유우까압","유우깝","유우방",
    "유우우방것","육갑","은년","은새끼","음경","이년","이새끼","자기핧아","자압것","자위","자지","자지구녕","자지구멍","자지꽂아","자지넣자","자지뜨더","자지뜯어","자지박어","자지빨아",
    "자지빨아줘","자지빨어","자지쑤셔","자지쓰레기","자지정개","자지짤라","자지털","자지핧아","자지핧아줘","자지핧어","작은보지","잠지","짬지","잠지뚫어","잠지물마셔","잠지털","잠짓물마셔",
    "잡것","잡년","잡놈","저년","저엇","저엊","적까","절라","점물","젓가튼쉐이","젓같내","젓까","젓냄새","젓대가리","젓떠","젓만이","젓물","젓물냄새","젓밥","정액마셔","정액먹어",
    "정액발사","정액짜","정액핧아","정자마셔","정자먹어","정자핧아","젖같","젖까","젖탱이","젗같","젼나","젼낰","졌같은","졏같","조가튼","조개넓은년","조개따조?","조개마셔줘?","조개벌려조?",
    "조개보지","조개속물","조개쑤셔줘?","조개핧아줘?","조깟","조또","조오가튼","조오까튼","조오또","조오오조","조오온니","조오올라","조오우까튼","조오웃","조오지","조온","조온나",
    "조온니","조온마니","조온만","조올라","조옴마니","조옷만","조우까튼","족같내","족까","족까내","존.나","존ㄴ나","존귀","존귘","존나","존나아","존낙","존내","존니","존똑","존마니",
    "존맛","존멋","존버","존싫","존쎄","존쎼","존예","존웃","존잘","존잼","존좋","존트","졸귀","졸귘","졸라","졸맛","졸멋","졸싫","졸예","졸웃","졸잼","졸좋","좀마니","좀물","좀쓰레기",
    "좁밥","좁빠라라","좃","좃가튼뇬","좃간년","좃까","좃까리","좃깟네","좃냄새","좃넘","좃대가리","좃도","좃또","좃마무리","좃만아","좃만이","좃만한것","좃만한쉐이","좃물","좃물냄새",
    "좃보지","좃부랄","좃빠구리","좃빠네","좃빠라라","좃털","종나","좆","좆같은놈","좆같은새끼","좆까","좆까라","좆나","좆년","좆도","좆만아","좆만한년","좆만한놈","좆만한새끼","좆먹어",
    "좆물","좆밥","좆빨아","좆새끼","좆털","좇","좋만","좋만한것","좋오웃","죠낸","죠온나","죤나","죤내","죵나","죶","주글년","주길년","주둥이","주둥아리","줬같은","쥐랄","쥰나",
    "쥰내","쥰니","쥰트","즤랄","지껄이","지랄","ㅈ1랄","지럴","지롤","지뢀","지뢰","지이라알","지이랄","짱깨","짱께","쪼녜","쪼다","쪼다새끼","쪽바리","쪽발","쫂","쫓같","쬰잘",
    "쬲","찝째끼","창남","창녀","창녀버지","창년","창년벼지","창놈","처먹","첫빠","쳐마","쳐먹","쳐받는","쳐발라","쳐쑤셔박어","촌씨브라리","촌씨브랑이","촌씨브랭이","취ㅈ","취좃",
    "친구년","친년","친노마","친놈","캐럿닷컴","크리토리스","큰보지","클리토리스","터래기터래기","파친","펑글","페니스","항문","항문수셔","항문쑤셔","허버리년","허벌","허벌년","허벌레",
    "허벌보지","허벌자식","허벌자지","허어벌","헐렁보지","혀로보지핧기","호냥년","호로","호로새끼","호로자","호로자슥","호로자식","호로잡","호루자슥","화낭년","화냥년","후.려","후라덜",
    "후라덜넘","후려","후우자앙","후우장","후장","후장꽂아","후장뚫어","후장뚫어18세키","꽃휴","sibal","미칭럼","ㅂㅅ","걔섀","느금","느금마","늑음","ㅈ같","ㅈ같네","ㅗ"]    

# 상태 사전 불러오기
state_dict = torch.load('C:/dev/miniproject/mysite/mysite/model/model_emotion.pth', map_location=torch.device('cpu'))

# 상태 사전에서 임베딩 가중치 가져오기
embeddings_weight = state_dict['bert.embeddings.word_embeddings.weight']

# 새로운 임베딩 가중치 크기로 조정
new_embeddings_weight = embeddings_weight[:30522, :]

# 상태 사전에서 임베딩 가중치 업데이트
state_dict['bert.embeddings.word_embeddings.weight'] = new_embeddings_weight

# 새로운 모델 불러오기
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

# 모델의 다른 가중치들을 불러온 상태 사전으로 업데이트
model.load_state_dict(state_dict, strict=False)

# 모델을 평가 모드로 설정
model.eval()

# 모델의 가중치 크기 비교
for name, param in model.named_parameters():
    if name in state_dict:
        print(f"Parameter name: {name}, Model shape: {param.shape}, State dict shape: {state_dict[name].shape}, Matches: {param.shape == state_dict[name].shape}")
    else:
        print(f"Parameter name: {name}, No matching entry in state dict")

## 입력 데이터 변환
def convert_input_data(sentences):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]
    MAX_LEN = 128
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
    attention_masks = []
    for seq in input_ids:
        seq_mask = [float(i > 0) for i in seq]
        attention_masks.append(seq_mask)
    inputs = torch.tensor(input_ids)
    masks = torch.tensor(attention_masks)
    return inputs, masks

# 문장 테스트
def test_sentences(sentences):
    model.eval()
    inputs, masks = convert_input_data(sentences)
    b_input_ids = inputs
    b_input_mask = masks
    with torch.no_grad():
        outputs = model(b_input_ids,
                        token_type_ids=None,
                        attention_mask=b_input_mask)
    logits = outputs[0]
    logits = logits.detach().cpu().numpy()
    return np.argmax(logits)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            #answer.add_emoji_based_on_sentiment()
            sentiment = test_sentences([answer.content])
            emoji = '😊' if sentiment == 1 else '😞'
            answer.content = answer.content + emoji
            
            for i in lst :
                if i in answer.content: 
                    answer.content = "비속어가 포함된 댓글입니다."
                else : 
                    answer.content
            answer.save()
            return redirect('{}#answer_{}'.format( 
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

@login_required(login_url='common:login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.all()
    

    
    context = {'question': question, 'answers': answers}
    return render(request, 'pybo/question_detail.html', context)