import axios from "axios";
import { API_URL } from "../constants";

const postUpgradePlan = (planName: string) => {
  axios
    .post(
      API_URL + "/payment/create_payment",
      {
        upgrade_plan_name: planName,
      },
      {
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      },
    )
    .then((res) => {
      window.location.replace(res.data.payment_url);
    })
    .catch((e) => {});
};

export { postUpgradePlan };
