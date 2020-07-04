%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
int yyerror(char *s);
int check_var_name(char *s);
extern FILE* yyin;
char var_name[30];
int value;
%}

%union {
    char name[30];
    int val;
}

%token INTEGER 
%token NAME 
%token EQ OP_PLUS OP_MINUS OP_MUL OP_DIV
%token NEWLINE
%left '-' '+'
%left '*' '/'

%type<val> INTEGER CMD
%type<name> NAME

%start Line
%%

Line: 
    CMD CMD { printf("%d", $2); exit(0); }
;
CMD: 
    NAME EQ INTEGER NEWLINE                 { sscanf($1, "%s", var_name); value = $3;}
    | NAME OP_PLUS INTEGER          { check_var_name($1); $$ = value + $3; }
    | NAME OP_MINUS INTEGER         { check_var_name($1); $$ = value - $3; }
    | NAME OP_MUL INTEGER           { check_var_name($1); $$ = value * $3; }
    | NAME OP_DIV INTEGER           {   check_var_name($1); 
                                        if ($3 == 0) {printf("INF"); exit(1);};
                                        $$ = value / $3; }
;
;
%%

int check_var_name(char *s)
{
    if (strcmp(s, var_name)) {
        printf("Variable \"%s\" is not declared", s);
        exit(1);
    };
}

int yyerror(char *s)
{
    fprintf(stderr, "%s\n", s);
}

int main()
{
    FILE *myfile = fopen("test.file", "r");
    
    if (!myfile) {
        printf("Can't open test.file");
        return -1;
    }
    
    yyin = myfile;
    // yyin = stdin;
	// do {
		yyparse();
	// } while(!feof(yyin));
	return 0;
}






