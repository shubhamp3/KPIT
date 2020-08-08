from __future__ import absolute_import, print_function
import sys, argparse, traceback, os, copy
if __name__ == '__main__' and __package__ is None:
    sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from preprocessor import Preprocessor, OutputDirective, Action

version='1.21'

__all__ = []


class ClearPreCompileCheck(Preprocessor):
    def __init__(self):
        self.lastdirective = None
        self.lexer = None
        self.define("__PCPP_ALWAYS_FALSE__ 0")
        self.define("__PCPP_ALWAYS_TRUE__ 1")
        self.bypass_ifpassthru = False
        self.potential_include_guard = None


    def on_error(self,file,line,msg):
        """Called when the preprocessor has encountered an error, e.g. malformed input.
        
        The default simply prints to stderr and increments the return code.
        """
        print("%s:%d error: %s" % (file,line,msg), file = sys.stderr)
        self.return_code += 1

        
    def on_include_not_found(self,is_system_include,curdir,includepath):
        """Called when a #include wasn't found.
        
        Raise OutputDirective to pass through or remove, else return
        a suitable path. Remember that Preprocessor.add_path() lets you add search paths.
        
        The default calls self.on_error() with a suitable error message about the
        include file not found and raises OutputDirective (pass through).
        """
        # self.on_error(self.lastdirective.source,self.lastdirective.lineno, "Include file '%s' not found" % includepath)
        raise OutputDirective(Action.IgnoreAndPassThrough)


    def on_unknown_macro_in_defined_expr(self,tok):
        """Called when an expression passed to an #if contained a defined operator
        performed on something unknown.
        
        Return True if to treat it as defined, False if to treat it as undefined,
        raise OutputDirective to pass through without execution, or return None to
        pass through the mostly expanded #if expression apart from the unknown defined.
        
        The default returns False, as per the C standard.
        """
        return None  # Pass through as expanded as possible
        
    def on_unknown_macro_in_expr(self,tok):
        """Called when an expression passed to an #if contained something unknown.
        
        Return what value it should be, raise OutputDirective to pass through
        without execution, or return None to pass through the mostly expanded #if
        expression apart from the unknown item.

        """
        return None  # Pass through as expanded as possible
        
    def on_directive_handle(self,directive,toks,ifpassthru,precedingtoks):
        """Called when there is one of
        
        define, include, undef, ifdef, ifndef, if, elif, else, endif
        
        Return True to execute and remove from the output, raise OutputDirective
        to pass through or remove without execution, or return None to execute
        AND pass through to the output (this only works for #define, #undef).
        
        The default returns True (execute and remove from the output).

        directive is the directive, toks is the tokens after the directive,
        ifpassthru is whether we are in passthru mode, precedingtoks is the
        tokens preceding the directive from the # token until the directive.
        """
        if ifpassthru:
            if directive.value == 'if' or directive.value == 'elif' or directive == 'else' or directive.value == 'endif':
                self.bypass_ifpassthru = len([tok for tok in toks if tok.value == '__PCPP_ALWAYS_FALSE__' or tok.value == '__PCPP_ALWAYS_TRUE__']) > 0
            if not self.bypass_ifpassthru and (directive.value == 'define' or directive.value == 'undef'):
                if toks[0].value != self.potential_include_guard:
                    raise OutputDirective(Action.IgnoreAndPassThrough)  # Don't execute anything with effects when inside an #if expr with undefined macro
                    
        if (directive.value == 'define' or directive.value == 'undef'):
            raise OutputDirective(Action.IgnoreAndPassThrough)

        return None  # Pass through where possible

    def on_directive_unknown(self,directive,toks,ifpassthru,precedingtoks):
        """Called when the preprocessor encounters a #directive it doesn't understand.
        This is actually quite an extensive list as it currently only understands:
        
        define, include, undef, ifdef, ifndef, if, elif, else, endif
        
        Return True to remove from the output, raise OutputDirective
        to pass through or remove, or return None to
        pass through into the output.
        
        The default handles #error and #warning by printing to stderr and returning True
        (remove from output). For everything else it returns None (pass through into output).

        directive is the directive, toks is the tokens after the directive,
        ifpassthru is whether we are in passthru mode, precedingtoks is the
        tokens preceding the directive from the # token until the directive.
        """
        if ifpassthru:
            return None  # Pass through
            
    def on_potential_include_guard(self,macro):
        """Called when the preprocessor encounters an #ifndef macro or an #if !defined(macro)
        as the first non-whitespace thing in a file. Unlike the other hooks, macro is a string,
        not a token.
        """
        self.potential_include_guard = macro        

    def on_comment(self,tok):
        return True  # Pass through

# def main():
    # p = CmdPreprocessor(sys.argv)
    # sys.exit(p.return_code)
        
# if __name__ == "__main__":
    # p = CmdPreprocessor(sys.argv)
    # sys.exit(p.return_code)
