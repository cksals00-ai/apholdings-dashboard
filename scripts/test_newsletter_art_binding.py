import copy,tempfile,unittest
from pathlib import Path
import test_newsletter_art_direction as fixtures
from newsletter_art_binding import reconcile_art_bindings
class BindingTests(unittest.TestCase):
 def test_reorder_preserves_bytes_and_reindexes_plans(self):
  self.run_case([1,0,2,3,4],None,[b'1',b'0',b'2',b'3',b'4'],False)
 def test_changed_source_archives_only_affected_and_hero(self):
  self.run_case([0,1,2,3,4],0,[None,b'1',b'2',b'3',b'4'],True)
 def test_changed_nonlead_keeps_hero(self):
  self.run_case([0,1,2,3,4],3,[b'0',b'1',b'2',None,b'4'],False)
 def run_case(self,order,changed,expected,hero_changed):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);folder=root/'state';images=root/'img/newsletter';images.mkdir(parents=True)
   old=[{'url':str(i),'summary':'summary','fact':'fact','title':'old'} for i in range(5)]
   stories=[copy.deepcopy(old[i]) for i in order]
   if changed is not None:stories[changed]['fact']='new fact'
   for i in range(5):(images/f'day-story-{i+1}.png').write_bytes(str(i).encode())
   for suffix in ('original.png','png','gif'):(images/f'day-hero-{suffix}' if suffix=='original.png' else images/f'day-hero.{suffix}').write_bytes(b'hero')
   state={'stories':stories,'editorial':{'lead_index':order.index(0)},'art_plans':fixtures.ArtDirectionTests().plans()}
   reconcile_art_bindings(root,folder,'day',state,old,{'lead_index':0})
   for i,value in enumerate(expected):
    p=images/f'day-story-{i+1}.png'
    self.assertEqual(p.read_bytes() if p.exists() else None,value)
   self.assertEqual((images/'day-hero.png').exists(),not hero_changed)
   self.assertEqual([p['story_index'] for p in state['art_plans']],list(range(6)))
   if changed is not None:self.assertIn(changed,[p['story_index'] for p in [state['pending_art_repair']]+state.get('art_repair_queue',[])])
   before=copy.deepcopy(state);reconcile_art_bindings(root,folder,'day',state,old,{'lead_index':0});self.assertEqual(state,before)
 def test_partial_destination_move_recovers_without_losing_bytes(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);images=root/'img/newsletter';images.mkdir(parents=True)
   old=[{'url':str(i),'summary':'s','fact':'f'} for i in range(5)]
   state={'stories':[old[1],old[0]]+old[2:],'editorial':{'lead_index':1},'art_plans':fixtures.ArtDirectionTests().plans()}
   for i in range(5):(images/f'day-story-{i+1}.png').write_bytes(str(i).encode())
   original=Path.replace;applied=0
   def flaky(path,target):
    nonlocal applied
    if 'art-bindings' in str(path) and str(target).endswith('.png'):
     applied+=1
     if applied==2:raise OSError('interrupted disk move')
    return original(path,target)
   with patch.object(Path,'replace',flaky),self.assertRaises(OSError):reconcile_art_bindings(root,root/'state','day',state,old,{'lead_index':0})
   reconcile_art_bindings(root,root/'state','day',state,old,{'lead_index':0})
   self.assertEqual([(images/f'day-story-{i+1}.png').read_bytes() for i in range(5)],[b'1',b'0',b'2',b'3',b'4'])
 def test_headline_only_change_preserves_assets_and_plan(self):
  old=[{'url':str(i),'summary':'s','fact':'f'} for i in range(5)]
  state={'stories':[dict(s,title='new') for s in old],'editorial':{'lead_index':0},'art_plans':fixtures.ArtDirectionTests().plans()}
  with tempfile.TemporaryDirectory() as d:
   reconcile_art_bindings(d,d,'day',state,old,{'lead_index':0})
  self.assertNotIn('pending_art_repair',state)
if __name__=='__main__':unittest.main()
