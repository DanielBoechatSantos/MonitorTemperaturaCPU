#include <windows.h>
#include <wbemidl.h>
#include <iostream>

extern "C" {
    __declspec(dllexport) float get_cpu_temperature() {
        HRESULT hres;
        hres = CoInitializeEx(0, COINIT_MULTITHREADED);
        if (FAILED(hres)) return -1.0f;

        hres = CoInitializeSecurity(NULL, -1, NULL, NULL, RPC_C_AUTHN_LEVEL_DEFAULT, 
                                   RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE, NULL);

        IWbemLocator *pLoc = NULL;
        hres = CoCreateInstance(CLSID_WbemLocator, 0, CLSCTX_INPROC_SERVER, IID_IWbemLocator, (LPVOID *)&pLoc);
        if (FAILED(hres)) { CoUninitialize(); return -2.0f; }

        IWbemServices *pSvc = NULL;
        // Substituído _bstr_t por BSTR simples para compatibilidade
        BSTR namespacePath = SysAllocString(L"ROOT\\WMI");
        hres = pLoc->ConnectServer(namespacePath, NULL, NULL, 0, NULL, 0, 0, &pSvc);
        SysFreeString(namespacePath);

        if (FAILED(hres)) { pLoc->Release(); CoUninitialize(); return -3.0f; }

        IEnumWbemClassObject* pEnumerator = NULL;
        BSTR language = SysAllocString(L"WQL");
        BSTR query = SysAllocString(L"SELECT CurrentTemperature FROM MSAcpi_ThermalZoneTemperature");
        
        hres = pSvc->ExecQuery(language, query, WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY, NULL, &pEnumerator);
        
        SysFreeString(language);
        SysFreeString(query);

        float tempC = 0.0f;
        if (SUCCEEDED(hres)) {
            IWbemClassObject *pclsObj = NULL;
            ULONG uReturn = 0;
            while (pEnumerator) {
                hres = pEnumerator->Next(WBEM_INFINITE, 1, &pclsObj, &uReturn);
                if (0 == uReturn) break;

                VARIANT vtProp;
                pclsObj->Get(L"CurrentTemperature", 0, &vtProp, 0, 0);
                tempC = (vtProp.uintVal - 2732) / 10.0f;
                
                VariantClear(&vtProp);
                pclsObj->Release();
                break;
            }
        }

        pSvc->Release();
        pLoc->Release();
        if(pEnumerator) pEnumerator->Release();
        CoUninitialize();

        return tempC;
    }
}