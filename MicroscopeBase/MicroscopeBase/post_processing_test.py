
import os
import dotnet.seamless

dotnet.add_assemblies('C:\\Users\\Huafeng\\Desktop\\VGitHub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase')
dotnet.load_assembly('MicroscopeAnalyzerLibrary')
import MicroscopeAnalyzerLibrary


def main():
    from_dir = 'C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\xmlfiles\\'
    relevant_files = [filename for filename in os.listdir(from_dir) if filename.startswith("Columbus") and filename.endswith(".xml")]

    to_dir = 'C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\Analysis_Columbus.txt'
    output_file = open(to_dir, 'w')
    
    print relevant_files

    for file in relevant_files:
        test_result = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer.LoadResultsFrom(from_dir + file)
        print file + " Layer_Thicknesses {}\n".format([i for i in test_result.LayerThicknesses])
        output_file.write(file + " Layer_Thicknesses {}\n".format([i for i in test_result.LayerThicknesses]))


    output_file.close()

    # print "PrimarySpectrum"
    # for e in testResult1.PrimarySpectrum: print e

    # print "Hello, world!"

main()