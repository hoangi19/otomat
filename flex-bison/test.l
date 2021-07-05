%option noyywrap

%{
#include <stdio.h>

#include <string.h>
#include "test.tab.h"

void error();
%}

%%
[[:blank:]\r]+
[_a-zA-Z][_a-zA-Z0-9]{0,30}    {sscanf(yytext, "%s", yylval.name); return(NAME);}
(--)*(0|[1-9][0-9]*)        {yylval.val=atoi(yytext); return(INTEGER);}
[\r\n]          {return(NEWLINE);}
"="             {return(EQ);}
"+"             {return(OP_PLUS);}
"-"             {return(OP_MINUS);}
"*"             {return(OP_MUL);}
"/"             {return(OP_DIV);}
"%"             {return(OP_MOD);}
.               {error(); return *yytext;}
%%

void error()
{
    printf("Parse error.");
}
