%option noyywrap

%{
#include <stdio.h>

#define YY_DECL int yylex()
#include <string.h>
#include "test.tab.h"

void error();
%}

%%
[[:blank:]\r]+
[_a-zA-Z][_a-zA-Z0-9]{0,30}    {sscanf(yytext, "%s", yylval.name); return(NAME);}
(--)*(0|[1-9][0-9]*)        {yylval.val=atoi(yytext); return(INTEGER);}

"="             {return(EQ);}
"+"             {return(OP_PLUS);}
"-"             {return(OP_MINUS);}
"*"             {return(OP_MUL);}
"/"             {return(OP_DIV);}
.               {error(); return *yytext;}
%%

void error()
{
    printf("Parse error.");
}
