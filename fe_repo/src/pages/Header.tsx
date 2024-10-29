import {GoogleLogin} from "@react-oauth/google";
import {hasUserId, setUserId} from "../functions/api.ts";


export const Header = () => {

  return (
    <div className="border-2 p-fined text-3xl font-bold p-4 bg-white rounded-lg shadow-md text-center text-gray-800">
      <span>CVCoach - Your best assistant for job seeking</span>

      {hasUserId() ? <GoogleLogin
        onSuccess={async (response) => {
          console.log("Google Login Success", response);
          if (response.credential) {
            setUserId(response.credential);
          }
        }}
        onError={() => console.log("Google Login Error")}
        useOneTap
      /> : null}

    </div>
  )
}

