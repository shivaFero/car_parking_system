export function responseHandler(res) {
  let obj = {};
  if (res.data && typeof res.data == typeof {}) {
    obj.data = res.data;
    if (res.data?.data) {
      obj.data = res.data.data;
    }
    if (res.data?.count) {
      obj.count = res.data.count;
    }
  } else {
    obj = res;
  }
  return obj;
}

export function errorHandler(err) {
  console.error(err);
  let obj = {};
  if (err.response.data) {
    obj.data = err.response.data;
    if (obj.data.error) {
      obj.data = err.response.data.error;
    }
  }
  obj.status = err.response.status;
  return obj;
}

export function setDataInLocalStorage(data, keyName) {
  localStorage.setItem(keyName, JSON.stringify(data));
}
export function getDataFromLocalStorage(keyName) {
  return JSON.parse(localStorage.getItem(keyName));
}
export function removeDataFromLocalStorage(keyName) {
  localStorage.removeItem(keyName);
}

export function getLoginUserDetails() {
  return getDataFromLocalStorage("user_credentials");
}
