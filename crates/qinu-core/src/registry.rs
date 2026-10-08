use std::collections::BTreeMap;
use crate::AlgorithmFamily;

#[derive(Default)]
pub struct Registry {
    suites: BTreeMap<String,(AlgorithmFamily,bool)>
}
impl Registry {
    pub fn register(&mut self, id:&str, family:AlgorithmFamily) -> bool {
        if self.suites.contains_key(id) { return false; }
        self.suites.insert(id.to_string(),(family,false)); true
    }
    pub fn deprecate(&mut self,id:&str)->bool {
        match self.suites.get_mut(id) { Some(v)=>{v.1=true;true}, None=>false }
    }
    pub fn get(&self,id:&str)->Option<(AlgorithmFamily,bool)> { self.suites.get(id).copied() }
}
