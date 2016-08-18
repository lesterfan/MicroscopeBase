import dotnet.seamless

dotnet.add_assemblies('C:\\Users\\Huafeng\\Desktop\\VGitHub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase')
dotnet.load_assembly('MicroscopeAnalyzerLibrary')
import MicroscopeAnalyzerLibrary

def main():
    testResult1 = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer.LoadResultsFrom("C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\xmlfiles\\Columbus_0_0.xml")

    # print "PrimarySpectrum"
    # for e in testResult1.PrimarySpectrum: print e
    print testResult1.ResultsSummary

    # print "Hello, world!"

main()