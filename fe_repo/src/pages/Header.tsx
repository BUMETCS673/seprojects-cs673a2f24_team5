import {GoogleLogin} from "@react-oauth/google";
import {hasUserId, login, setUserId} from "../functions/api.ts";
import {useState} from "react";


export const Header = () => {

  const [refreshPage, setRefreshPage] = useState(false);

  return (
    <div className="border-2 p-fined text-3xl font-bold p-4 bg-white rounded-lg shadow-md text-center text-gray-800">
      <span>CVCoach - Your best assistant for job seeking</span>

      {!hasUserId() ? <GoogleLogin
        onSuccess={async (response) => {
          console.log("Google Login Success", response);
          if (response.credential) {
            const user_id = await login(response.credential);
            if (user_id) {
              setUserId(user_id);
            } else {
              setUserId(response.credential);
            }
            setRefreshPage(!refreshPage);
          }
        }}
        onError={() => console.log("Google Login Error")}
      /> : null}

    </div>
  )
}

