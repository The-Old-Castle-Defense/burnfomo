import { defineStore } from "pinia";
import Web3 from "web3";

export const useMain = defineStore("main", () => {

  const FOMOContractAddress = "0xa7ea9d5d4d4c7cF7dbde5871E6D108603C6942a5";
  const BURNAccAddress = "0x44038cb60e83c45696324B0791B841A4dC844041"

  const state = reactive({
    fetchRateLastUpdate: 0,
    burgerIsActive: false,
  })

  const erc20Abi = [
    {
      "constant": true,
      "inputs": [
        {
          "name": "_owner",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "name": "balance",
          "type": "uint256"
        }
      ],
      "type": "function"
    }
  ];

  const web3 = new Web3('https://base-rpc.publicnode.com');

  async function getBalances() {
    const erc20Contract = new web3.eth.Contract(erc20Abi, FOMOContractAddress);
    try {
      // get balance ETH
      let ethBalance = await web3.eth.getBalance(BURNAccAddress);
      ethBalance = web3.utils.fromWei(ethBalance, 'ether')

      // get balance ERC-20 token
      let erc20Balance = await erc20Contract.methods.balanceOf(BURNAccAddress).call();
      erc20Balance = web3.utils.fromWei(erc20Balance, 'ether')
      return [ethBalance, erc20Balance];
    } catch (error) {
      console.error('Error fetching balances:', error);
    }
  }



  const getBurnStatistics = async () => {
    try {
      const response = await $fetch('https://burnfomo.theoldcastle.xyz/api/burn_statistics')
      console.log('response', response)
      return response
    } catch (e) {
      console.error(e)
    }
  }

  const timeForFetchRate = 5;

  const setCookie = (name, value, minutes) => {
    let expires = "";
    if (minutes) {
      let date = new Date();
      date.setTime(date.getTime() + minutes * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }

    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  };

  const getCookie = (cName) => {
    const name = cName + "=";
    const cDecoded = decodeURIComponent(document.cookie);
    const cArr = cDecoded.split("; ");
    let res;
    cArr.forEach((val) => {
      if (val.indexOf(name) === 0) res = val.substring(name.length);
    });
    return res;
  };


  const getETHRate = async () => {
    try {
      const cacheRate = getCookie("ETHRate");
      let rate;
      if (!cacheRate) {
        rate = await $fetch(`https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd`);
        rate = rate.ethereum?.usd
        setCookie("ETHRate", rate, timeForFetchRate);
      } else {
        rate = cacheRate;
      }
      return rate;
    } catch (e){
      console.error(e)
      return 0
    }
  }

  const getFOMORate = async () => {
    try {
      let rate;
      const cacheRate = getCookie("fomoRate");

      if (!cacheRate) {
        rate = await $fetch(`https://api.geckoterminal.com/api/v2/simple/networks/base/token_price/${FOMOContractAddress}`);
        rate = rate?.data?.attributes?.token_prices?.[FOMOContractAddress.toLowerCase()];
        setCookie("fomoRate", rate, timeForFetchRate);

        let lastUpdateMinutes = Math.floor(Date.now() / 60000);
        setCookie("lastUpdateMinutes", lastUpdateMinutes, timeForFetchRate);
      } else {
        rate = cacheRate;
      }

      const lastUpdateMinutes = getCookie("lastUpdateMinutes");
      if (lastUpdateMinutes !== null) {
        const nowMinutes = Math.floor(Date.now() / 60000);
        const minutesSinceLastUpdate = nowMinutes - parseInt(lastUpdateMinutes);
        state.fetchRateLastUpdate = minutesSinceLastUpdate;
      } else {
        state.fetchRateLastUpdate = "N/A";
      }

      return rate;
    } catch (e) {
      console.error(e);
      return 0;
    }
  };


  const myToFixed = (num, to_fix = 2) => {
    if (typeof num === "number" && !isNaN(num)) {
      const numStr = num.toFixed(to_fix);
      const [integerPart, decimalPart] = numStr.split(".");
      const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      const formattedDecimalPart = decimalPart ? `.${decimalPart}` : "";
      return `${formattedIntegerPart}${formattedDecimalPart}`;
    } else if (typeof num === "string") {
      const parsedNum = parseFloat(num);
      if (!isNaN(parsedNum)) {
        const numStr = parsedNum.toFixed(to_fix);
        const [integerPart, decimalPart] = numStr.split(".");
        const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        const formattedDecimalPart = decimalPart ? `.${decimalPart}` : "";
        return `${formattedIntegerPart}${formattedDecimalPart}`;
      }
    }
  };

  const DateToRead = (timestamp, isUnix = false) => {
    let dateObj
    if (isUnix) {
      dateObj = new Date(timestamp);
    } else {
      dateObj = new Date(timestamp * 1000);
    }

    const year = dateObj.getFullYear();
    const month = (dateObj.getMonth() + 1).toString().padStart(2, "0");
    const day = dateObj.getDate().toString().padStart(2, "0");
    const hours = dateObj.getHours().toString().padStart(2, "0");
    const minutes = dateObj.getMinutes().toString().padStart(2, "0");

    return `${day}.${month}.${year} ${hours}:${minutes}`;
  };

  const toggleBurger = () => {
    state.burgerIsActive = !state.burgerIsActive
    if (state.burgerIsActive){
      document.querySelector('body').classList.add('_active')
    } else {
      document.querySelector('body').classList.remove('_active')
    }
  }

  const formatNumberToString = (number, fromNumber = 1000, decimals = 2) => {
    if (number < fromNumber) {
      return myToFixed(number, decimals);
    } else if (number < 1000000) {
      return myToFixed(number / 1000, decimals) + 'K';
    } else if (number < 1000000000) {
      return myToFixed(number / 1000000, decimals) + 'M';
    } else {
      return myToFixed(number / 1000000000, decimals) + 'B';
    }
  }

  const cropText = (str, slice = 10) => {
    if (!str || str.length === 0) return "";
    if (str.length > str.length - 1) str = str.slice(0, 6) + "..." + str.slice(-str.length / slice);
    return str;
  };

  const scrollToElement = (elementId) => {
    const scrollTarget = document.getElementById(elementId);
    if (scrollTarget) {
      const scrollOptions = {
        top: scrollTarget.offsetTop,
        behavior: 'smooth'
      };
      window.scrollTo(scrollOptions);
    }
  };


  return {
    state,
    myToFixed,
    getBurnStatistics,
    FOMOContractAddress,
    getFOMORate,
    setCookie,
    DateToRead,
    formatNumberToString,
    cropText,
    scrollToElement,
    getBalances,
    getETHRate,
    toggleBurger
  }
})