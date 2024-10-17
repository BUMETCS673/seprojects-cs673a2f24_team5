import {UploadIcon} from "../icons"
import {Textarea} from '../components'
import {useState} from "react";
import {uploadFile} from "../functions/api.ts";

interface IChatBoxProps {
  onSendMessage: (message: string) => void;
  onAnalyze: (jd: string) => void;
}

export const ChatBox = ({onSendMessage, onAnalyze}: IChatBoxProps) => {

  const [message, setMessage] = useState("");
  const [showPrompt, setShowPrompt] = useState(false);
  const [jobDescription, setJobDescription] = useState("");

  const handleSend = () => {
    if (message.trim() == "") {
      return;
    }
    // call upper function to send message
    onSendMessage(message);
    setMessage("");
  }

  const handleAnalyze = () => {
    if (jobDescription.trim() !== "") {
      // Call the analyze function with job description
      onAnalyze(jobDescription);
    }
    setShowPrompt(false);
    setJobDescription(""); // Clear the input after submission
  };


  return (
    <div className="border-2 p-4 flex flex-col bg-white rounded-lg shadow-md">
      {/* Overlay and Modal for Job Description */
        showPrompt && (
          <>
            <div
              className="fixed inset-0 bg-black bg-opacity-50 z-40"
              onClick={() => setShowPrompt(false)}
            />
            <div
              className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-10 rounded-xl shadow-xl z-50 w-96">
              <h3 className="text-2xl font-bold mb-6">Enter a Job Description</h3>
              <Textarea
                className="w-full h-40 p-4 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-all"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Enter job description here..."
              />
              <button
                className="mt-6 bg-blue-500 text-white font-semibold text-lg px-8 py-3 rounded-lg shadow-md hover:bg-blue-600 hover:shadow-lg transition-all w-full"
                onClick={handleAnalyze}
              >
                Submit
              </button>
            </div>

          </>
        )
      }
      {/* icon row */
      }
      <div className="flex justify-start gap-2 mb-2">
        <div
          style={{width: '64px', display: 'flex', justifyContent: 'center', cursor: 'pointer'}}
          onClick={() => {
            // Upload files
            const handleFiles = (event: Event) => {
              const files = (event.target as HTMLInputElement)?.files;
              if (!files || files.length === 0) return;
              const file = files[0];
              if (file) {
                // upload if file is valid
                uploadFile(file);
              }
            }

            const input = document.createElement("input");
            input.type = 'file';
            input.accept = '.pdf';
            input.onchange = handleFiles;
            input.click();
          }}
        >
          <UploadIcon/>
        </div>
        <button
          className="cursor-pointer px-4 py-2 rounded-full bg-blue-500 text-white text-sm flex items-center gap-1 hover:bg-blue-600 transition"
          onClick={() => setShowPrompt(true)}
        >
          <span className="text-base">📄</span> Analyze my resume
        </button>
        {/*🛈 /!* Example icon - you can use actual icons here *!/*/}
        {/*💼 /!* Example icon for interview *!/*/}
      </div>
      {/* input row */}
      <div style={{display: 'flex', alignItems: 'center'}}>
        <Textarea
          className="flex-1"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyUp={(e) => {
            // listen for enter key
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
      </div>
    </div>
  )
}

