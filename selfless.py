'''
selfless: A small experimental module for implicit "self" support in Python (in some restricted contexts)
'''
import sys, ast, inspect, types, textwrap, functools

class SelflessTransformer(ast.NodeTransformer):
    def __init__(self, variables, globals_dict, locals_dict):
        ast.NodeTransformer.__init__(self)
        
        self.selfless_variables = variables
        self.globals_dict = dict(globals_dict)
        self.globals_dict.update(locals_dict)
        self.local_names = set()
        self.builtins_names = dir(globals_dict['__builtins__'])
        self.found_variables = set()


    def visit_FunctionDef(self, node):
        local_names_original = set(self.local_names)
        for arg in node.args.args:
            self.local_names.add(arg.arg)

        if node.args.vararg is not None:
            self.local_names.add(node.args.vararg.arg)
            
        if node.args.kwarg is not None:
            self.local_names.add(node.args.kwarg.arg)

        for arg in node.args.kwonlyargs:
            self.local_names.add(arg.arg)
            
        for stmt in node.body:
            self.visit(stmt)
        
        self.local_names = local_names_original 
        return node
        
        
    def visit_Name(self, node):
        if self.selfless_variables:
            if node.id in self.selfless_variables:
                return ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=node.id, ctx=node.ctx)
                
        elif node.id not in self.local_names and node.id not in self.globals_dict and node.id not in self.builtins_names:
            if node.id[0] != '_':
                return ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=node.id, ctx=node.ctx)
            
        return node

        
class SelflessWithTransformer(ast.NodeTransformer):
    def __init__(self, variables, globals_dict, locals_dict):
        ast.NodeTransformer.__init__(self)
        
        self.selfless_variables = variables
        self.globals_dict = dict(globals_dict)
        self.globals_dict.update(locals_dict)
        self.local_names = set()
        self.builtins_names = dir(globals_dict['__builtins__'])
        self.found_variables = set()
        self.is_inside_with = False

    def visit_FunctionDef(self, node):
        local_names_original = set(self.local_names)
        for arg in node.args.args:
            self.local_names.add(arg.arg)

        if node.args.vararg is not None:
            self.local_names.add(node.args.vararg.arg)
            
        if node.args.kwarg is not None:
            self.local_names.add(node.args.kwarg.arg)

        for arg in node.args.kwonlyargs:
            self.local_names.add(arg.arg)
            
        for stmt in node.body:
            try:
                if len(stmt.items) == 1 and getattr(stmt.items[0].context_expr, 'id', None) == "selfless":
                    print('removing stmt')
                    for stmt2 in stmt.body:
                        print('visiting', stmt2)
                        self.visit(stmt2)
                        
                    del stmt
                        
                    continue
            except:
                pass
            
            self.visit(stmt)
        
        self.local_names = local_names_original 
        return node
        
        
    def visit_With(self, node):
        #print(node.items[0])
        # if len(node.items) == 1 and getattr(node.items[0].context_expr, 'id', None) == "selfless":
            # print('removing node')
            # return None#node.body
        return node
        
        
        
    def visit_Name(self, node):
        if self.is_inside_with:
            if self.selfless_variables:
                if node.id in self.selfless_variables:
                    return ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=node.id, ctx=node.ctx)
                    
            elif node.id not in self.local_names and node.id not in self.globals_dict and node.id not in self.builtins_names:
                if node.id[0] != '_':
                    return ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=node.id, ctx=node.ctx)
        
        else:
            if self.selfless_variables:
                if node.id in self.selfless_variables:
                    return ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=node.id, ctx=node.ctx)
                    
            elif node.id not in self.local_names and node.id not in self.globals_dict and node.id not in self.builtins_names:
                if node.id[0] != '_':
                    return ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=node.id, ctx=node.ctx)
            
        return node
        

        
def selfless(cls, variables=None, globals_dict=None, locals_dict=None, restrict_to_with=False):
    if variables is None:
        variables = getattr(cls, '_selfless', [])

    if globals_dict is None or locals_dict is None:
        frames = inspect.getouterframes(inspect.currentframe())
        # Note: the following block was rewritten to use indexing instead 
        #       of the attribute name (frame) for Python 2.7 compatibility
        if globals_dict is None:
            globals_dict = frames[1][0].f_globals
        if locals_dict is None:
            locals_dict = frames[1][0].f_locals
                
    src = inspect.getsource(cls)
    if src[0] in (' ', '\t'):
        src = textwrap.dedent(src)
        
    cls_ast_original = ast.parse(src)
    if restrict_to_with:
        cls_ast = SelflessWithTransformer(variables, globals_dict, locals_dict).visit(cls_ast_original)
    else:
        cls_ast = SelflessTransformer(variables, globals_dict, locals_dict).visit(cls_ast_original)
    
    cls_ast = ast.fix_missing_locations(cls_ast)
    compiled = compile(cls_ast, filename='<ast from {}>'.format(cls.__name__), mode="exec")
    globals_dict = dict(globals_dict)
    globals_dict.update(locals_dict)
    exec(compiled, globals_dict)
    return globals_dict[cls.__name__]
    
selfless_with = functools.partial(selfless, restrict_to_with=True)

    
