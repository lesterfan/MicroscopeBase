import dotnet.seamless

# Load the compiled C# library... see the C# library to see how everything works
dotnet.add_assemblies('C:\\Users\\HMNL\\Desktop\\VsGithub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase\\')
dotnet.load_assembly('MicroscopeAnalyzerLibrary')
import MicroscopeAnalyzerLibrary


def main():
    mAnalyzer = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer(True)
    if mAnalyzer.mLastRet == 1:
        print "Something wrong in the last step!"

    while True:
        input = raw_input( "Enter in 'a' to take measurement, enter in 's' to save, 'l' to load\n" )

        if input == 'a':
            print "Now measuring!"

            # Emulates click on the 'measure' button
            mAnalyzer.Measure()
            if mAnalyzer.mLastRet == 1:
                print "Something wrong in the last step!"
            else:
                print "Measurement successful!"

        elif input == 's':
            mAnalyzer.mMeasuredResults.ret = "Saved!"
    
            print "Please enter in the name of the file you want it to be saved in."
            print "The program will automatically save it as a '.fmspe' file. "
            print "For now, all files will be saved in directory 'C:/Users/HMNL/Documents/Test/' "

            currFileDir = "C:/Users/HMNL/Documents/Test/"
            user_input = raw_input("\n")

            # Save the .fmspe file
            mAnalyzer.SaveSpectrum(currFileDir, user_input)
            if mAnalyzer.mLastRet == 1:
                print "Something wrong in the last step!"

            # Save the .xml data structure and the image.
            mAnalyzer.SaveResultsTo(currFileDir, user_input)
            if mAnalyzer.mLastRet == 1:
                print "Something wrong in the last step!"

        elif input == 'l':
            print "Please enter in the name of the file you want the settings loaded from."
            print "For now, all files will be saved from directory 'C:/Users/HMNL/Documents/Test/' "
            
            currFileDir = "C:/Users/HMNL/Documents/Test/"
            user_input = raw_input("\n")

            # Load the result
            loaded_result = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer.LoadResultsFrom(currFileDir, user_input)
            if loaded_result == None:
                print "Something wrong in the last step"
                continue

            print "Load successful!"
            for item in loaded_result.PrimaryWavelengths:
                print item

            print "The summary is ", loaded_result.ResultsSummary

main()