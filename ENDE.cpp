#include "pch.h"
#include <stdio.h>
#include <stdlib.h>
#include <comdef.h> 
extern "C" __declspec(dllexport)
void encrypting(wchar_t* filename, int seedkey, unsigned long long int devide)
{
    unsigned long long int filesize = -1;
    unsigned long long int origin_size = -1;
    _bstr_t cc(filename);
    FILE* fp;
    fopen_s(&fp,cc, "rb");
    if (fp == 0)
        return ;
    fseek(fp, 0, SEEK_END);
    filesize = ftell(fp);
    fclose(fp);
    origin_size = filesize;
    unsigned char* data;
    data = (unsigned char*)malloc((unsigned long long int)(filesize));
    _bstr_t cc1(filename);
    FILE* fb;
    fopen_s(&fb, cc1, "rb");
    fread(data, 1, filesize, fb);
    fclose(fb);
    unsigned long long int* inds1;
    unsigned long long int* inds2;
    unsigned long long int ind1;
    unsigned long long int ind2;
    unsigned long long int temp;
    unsigned long long int i = 0;
    unsigned char t;
    unsigned char k;
    filesize = (unsigned long long int)(filesize / devide);
    srand(seedkey + 1);
    for (i = 0; i < filesize; i++)
    {
        t = data[i];
        k = ((unsigned char)(rand()) % 256);
        data[i] = t ^ k;
    }

    srand(seedkey);
    for (i = 0; i < filesize; i++)
    {
        ind1 = (unsigned long long int)((rand() * rand()) % (unsigned long long int)(filesize));
        ind2 = (unsigned long long int)((rand() * rand()) % (unsigned long long int)(filesize));
        temp = data[ind1];
        data[ind1] = data[ind2];
        data[ind2] = temp;
    }
    _bstr_t cc2(filename);
    FILE* frb;
    fopen_s(&frb, cc2, "wb");
    fwrite(data, 1, (origin_size), frb);
    fclose(frb);
}
extern "C" __declspec(dllexport)
void decrypting(wchar_t* filename, int seedkey, unsigned long long int divide)
{
    char datafilename[30] = "shuffle_data.bin";
    FILE* fbin;
    _bstr_t cc0(datafilename);
    fopen_s(&fbin, cc0, "wb");
    fwrite(0, 0, 0, fbin);
    fclose(fbin);
    unsigned long long int filesize;
    unsigned long long int origin_size;
    _bstr_t cc1(filename);
    FILE* fp;
    fopen_s(&fp, cc1, "rb");
    if (fp == 0)
        return (void)*filename;
    fseek(fp, 0, SEEK_END);
    filesize = ftell(fp);
    fclose(fp);
    origin_size = filesize;
    unsigned char* arr;
    arr = (unsigned char*)malloc(filesize);
    _bstr_t cc2(filename);
    FILE* fb;
    fopen_s(&fb, cc2, "rb");
    fread(arr, 1, filesize, fb);
    fclose(fb);
    unsigned long long int temp;
    unsigned long long int ind1, ind2;
    unsigned long long int* inds1, * inds2;
    unsigned long long int i;
    unsigned long long int cnt = 0;
    short fsize = 8;
    int run = 1;
    filesize = (unsigned long long int)(filesize / divide);
    _bstr_t cc3(datafilename);
    FILE* tfbin;
    fopen_s(&tfbin, cc3, "wb");
    srand(seedkey);
    for (i = 0; i < filesize; i++)
    {
        ind1 = (unsigned long long int)((rand() * rand()) % (unsigned long long int)(filesize));
        ind2 = (unsigned long long int)((rand() * rand()) % (unsigned long long int)(filesize));
        fwrite(&ind1, 8, 1, tfbin);
        fwrite(&ind2, 8, 1, tfbin);
    }
    fclose(tfbin);
    unsigned long long int a, b;
    _bstr_t cc4(datafilename);
    FILE* rtfbin;
    fopen_s(&rtfbin, cc4, "rb");

    fseek(rtfbin, 0, SEEK_END);
    fseek(rtfbin, -8, SEEK_CUR);
    while (cnt < filesize)
    {
        fread(&a, fsize, 1, rtfbin);
        fseek(rtfbin, -16, SEEK_CUR);
        fread(&b, fsize, 1, rtfbin);
        fseek(rtfbin, -16, SEEK_CUR);
        temp = arr[a];
        arr[a] = arr[b];
        arr[b] = temp;
        cnt++;
    }
    fclose(rtfbin);
    unsigned char t, k;
    srand(seedkey + 1);
    for (i = 0; i < filesize; i++)
    {
        t = arr[i];
        k = ((unsigned char)(rand()) % 256);
        arr[i] = t ^ k;
    }
    _bstr_t cc5(filename);
    FILE* fp2;
    fopen_s(&fp2, cc5, "wb");
    fwrite(arr, 1, origin_size, fp2);
    fclose(fp2);
    free(arr);
}
extern "C" __declspec(dllexport)
void ende(wchar_t* filename, int seedkey, unsigned long long int divide, int ed)
{
    if (ed)
        encrypting(filename, seedkey, divide);
    else
        decrypting(filename, seedkey, divide);
}