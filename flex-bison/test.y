%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
int yylex();
int yyerror(char *s);
int check_var_name(char *s);
extern FILE* yyin;
char var_name[30];      // ten bien nhap vao
char var_name1[30];     // ten bien thu 1
char var_name2[30];     // ten bien thu 2
char var_name3[30];     // ten bien thu 3
int value1;             // gia tri bien 1
int value2;             // ...
int value3;
int value;              // ket qua phep tinh
bool var_1_is_seted = false;        // true neu var_name1, value1 da co gia tri duoc luu
bool var_2_is_seted = false;        // ...
bool var_3_is_seted = false;
%}

%union {
    char name[30];
    int val;
}

%token INTEGER 
%token NAME 
%token EQ OP_PLUS OP_MINUS OP_MUL OP_DIV OP_MOD
%token NEWLINE
%type<val> INTEGER CMD
%type<name> NAME

%start Line
%%

Line: 
    CMD CMD CMD CMD { printf("%d", value); exit(0);}
;
CMD: 
    NAME EQ INTEGER NEWLINE                 { sscanf($1, "%s", var_name); init_value($3);}
    | NAME OP_PLUS NAME          {  value = get_value($1) + get_value($3); }
    | NAME OP_MINUS NAME         {  value = get_value($1) - get_value($3); }
    | NAME OP_MUL NAME           {  value = get_value($1) * get_value($3); }
    | NAME OP_MOD NAME           {  value = get_value($1) % get_value($3); }
    | NAME OP_DIV NAME           {  value = get_value($1) / get_value($3); }
;
;
%%
// gan gia tri moi vao bien
void init_value(int valtmp)
{
    // kiem tra bien nhap vao giong ten voi bien 1 hay ko
    if (strcmp(var_name, var_name1) == 0)
    {
        value1 = valtmp;
    } // kiem tra bien nhap vao giong ten voi bien 2 hay ko 
    else if (strcmp(var_name, var_name2) == 0)
    {
        value2 = valtmp;
    } // kiem tra bien nhap vao giong ten voi bien 3 hay ko
    else if (strcmp(var_name, var_name3) == 0)
    {
        value3 = valtmp;
    }
    else{ // neu ko giong thi tim bien chua duoc gan gia tri
        if (var_1_is_seted == false)
        {
            // copy ten va gia tri tu dong lenh vao bien 1
            memcpy(var_name1, var_name, 30);
            value1 = valtmp;
            var_1_is_seted = true;
        }
        else if (var_2_is_seted == false)
        {
            // copy ten va gia tri tu dong lenh vao bien 2
            memcpy(var_name2, var_name, 30);
            value2 = valtmp;
            var_2_is_seted = true;
        }
        else if (var_3_is_seted == false)
        {
            // copy ten va gia tri tu dong lenh vao bien 3
            memcpy(var_name3, var_name, 30);
            value3 = valtmp;
            var_3_is_seted = true;
        }
    };
}

// tim gia tri cua bien ( s la ten bien )
int get_value(char *s)
{
    if (strcmp(s, var_name1) == 0)
    {
        return value1;
    }
    else if (strcmp(s, var_name2) == 0)
    {
        return value2;
    }
    else if (strcmp(s, var_name3) == 0)
    {
        return value3;
    }
    else{
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






