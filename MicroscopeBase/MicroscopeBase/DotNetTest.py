import dotnet.seamless

dotnet.add_assemblies('C:\\Users\\Huafeng\\Desktop\\VGithub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase\\')
dotnet.print_pretty_names(dotnet.assemblies())

# Load the assembly
dotnet.load_assemblies('FIRemoteCOM')
# 
# 
dotnet.print_pretty_names(dotnet.namespaces("FIRemoteCOM"))
# 
# dotnet.build_assembly(FilmmetricsAnalysisString, 'FilmmetricsAnalysis.dll', ['FILMeasure.exe', 'System.Xml.dll', 'System.Drawing.dll'], '/debug')
# 
import FIRemoteCOM


def main():
    # mAnalyzer = FilmetricsAnalysis.MicroscopeAnalyzer(True)

    mFIRemote = FIRemoteCOM.FIRemote(True)


    print "Hello, world!"

main()