#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int change_last_bit(int val, int bit) {
    // change the last bit of an integer value to the specified bit
    return (val & ~1) | bit;
}

char* cov_time(int last_bit) {    

    // int last_bit = 1;  // get current binary value from list

    // get current timestamp and change its last bit based on binary value
    time_t current_time = time(NULL);
    struct tm *timeinfo = localtime(&current_time);

    // printf("Timestamp with un-modified last bit: ");
    // printf("%s", asctime(localtime(&current_time)));

    timeinfo->tm_sec = change_last_bit(timeinfo->tm_sec, last_bit);  // change last bit of seconds field
    current_time = mktime(timeinfo);
    // // print modified timestamp and binary value for each character
    // printf("Timestamp with modified last bit: ");
    // printf("%s", asctime(localtime(&current_time)));
    // printf("\n");

    // convert the timestamp to a Unix time
    time_t unix_time = (time_t)difftime(current_time, (time_t)0);
    // convert the Unix time to a hexadecimal string

    // //Convert this stack usage to heap usage
    // char hex_string[17];

    char* hex_string = (char*)malloc(17*sizeof(char));
    sprintf(hex_string, "%lx", unix_time);
    // printf("%s\n",hex_string);

    // // Convert Hex to Unsigned Int
    // unsigned int timestamp = strtoul(hex_string, NULL, 16);
    // printf("%u",timestamp);

    return hex_string;
}

int main(){
    char* hex_string = cov_time(0);
    printf("%s\n",hex_string);
}
