class SymbolTable:
   def __init__(self):
      self.class_table = []
      self.subroutine_table = []

   def define(self, name, type, kind):
      if type in ['static', 'field']:
         table = self.class_table
      else:
         table = self.subroutine_table
      
      index = len(list(filter(lambda x: x['kind'] == type, table)))

      table.append({'name': name, 'type':kind, 'kind':type, 'index':index})
   
   def start_subroutine(self):
      self.subroutine_table = []

   def type_of(self, string):
      type = filter(lambda x: x['name'] == string, self.subroutine_table + self.class_table)
      return list(type)[0]['type']
   
   def kind_of(self, string):
      type = filter(lambda x: x['name'] == string, self.subroutine_table + self.class_table)
      return list(type)[0]['kind']
   
   def index_of(self, string):
      type = filter(lambda x: x['name'] == string, self.subroutine_table + self.class_table)
      return list(type)[0]['index']
   
   def var_count(self, kind):
      filtered = filter(lambda x: x['kind'] == kind, self.subroutine_table + self.class_table)
      return len(list(filtered))
