from pathlib import Path
import json
xs=json.loads(Path('work/alignment-review.json').read_text(encoding='utf8')); mp=json.loads(Path('work/mapping.json').read_text(encoding='utf8'))
def resolve(g,ids):
 e=xs[g]['english'];k=xs[g]['korean'];assert len(e)==len(ids),(g,len(e),len(ids))
 for a,b in zip(e,ids):mp[a]=k[b] if isinstance(b,int) else b
resolve(0,['알겠어.',0]);resolve(1,[0,1,2,'다음 모임 때 함께 읽을 시를 써 와!'])
resolve(2,[0,1,2,3,4,'나도 내 시를 꺼냈다.']);resolve(3,[0,1,2,'아직은 그런 영감을 받지 못했거든요.']);resolve(4,[0,1,2,'그렇다면, 내가 고를 사람은…!'])
resolve(5,['나는 속으로 생각했다.',0,1,2]);resolve(6,[0,'솔직히 감탄했어.']);resolve(7,['교실을 둘러본다.',0,1])
resolve(8,['별 의미는 없는데… 만약 어느 날 [ch2_winner]가 집에 같이 가자고 한다면….'])
resolve(9,['음….',0,1]);resolve(10,[0,'내가 널 버리고 [ch2_winner]를 고를 거라고 생각한 거야?']);resolve(11,[0,1,'[ch2_winner]라면 그 정도는 해 줄 수 있지 않아…?'])
resolve(12,[0,1])
for e,k in zip(xs[13]['english'][1][1],xs[12]['korean'][2:]):mp[e]=k
resolve(14,[0])
resolve(15,[0,'물론 내가 고를 사람은…',1,'진짜로 [ch4_name]가 일요일 내 집으로 오는 거야…?',4,'그래도 내 집으로 온다는 생각에 긴장감이 지붕 끝까지 차오른다.',7,8,9,10,11,12,13,14,15,'긴장감이 지붕 끝까지 차오른다.',18,19,20,21,22,23,24,25])
resolve(16,list(range(15))+['물론 넌 지금 3DS에서 플레이하고 있지만….',17,18,19]+list(range(20,30)))
resolve(17,list(range(8))+[9,10,11,12,13]);resolve(18,list(range(4))+list(range(5,10)))
resolve(19,list(range(11))+[xs[19]['korean'][11]+' '+xs[19]['korean'][12],13,14])
resolve(20,list(range(9))+['생각해보니, 그거 꽤 유혹적인걸….','…아무튼, 그게 중요한 건 아니고!']+list(range(9,20)))
resolve(21,list(range(21))+['나는 [ch4_name]가 오기 전에 사요리를 찾아가 보기로 했다.']+list(range(23,30)))
resolve(22,[0,'오늘 [ch4_name]랑 만나는 거 아니었어?']);resolve(23,['아, 그럼 나랑 [ch4_name]만 만나는 거구나….']);resolve(24,[0,'거의 [ch4_name]랑 우리 집에서 보기로 한 시간이 됐고….',3,4]);resolve(25,[0,1,'그렇지만 [ch4_name]가 오는 마당에 계속 걱정하고 있기도 좀 그러니까….',4,5,6]);resolve(26,[0,'그건 어떤 기분일 때 쓰는 거야?']);resolve(27,[0,'네가 [ch4_name]랑 재밌는 시간을 보내는 거랑.']+list(range(3,7)))
resolve(30,list(range(7))+[9,10,7,'낭송회보다도, 사요리와 [ch4_name]랑 같이 축제를 즐길 생각에 벌써 마음이 들뜬다.',13]);resolve(31,[0,'조금 전에는 기대된다고 했잖아.']);resolve(32,list(range(40)))
for e,k in zip(xs[33]['english'][1][1],xs[32]['korean'][40:]):mp[e]=k
resolve(34,['누구에게 먼저 시를 보여줄까?']+list(range(8)));resolve(35,['나이 어린 여자애한테 참견을 허용한 결과가 이건가.',0,1]);resolve(36,[0,'시를 주는 건 괜찮은데, 그래도 [unfairto]한테는 좀 불공평한 거 아니야…?',3]);resolve(37,[0,1,2,'아마도… [currentname]?']);resolve(38,[0,0])
Path('work/mapping.json').write_text(json.dumps(mp,ensure_ascii=False,indent=2),encoding='utf8');print('mapping',len(mp))
