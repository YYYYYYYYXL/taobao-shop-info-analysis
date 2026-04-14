const _0x1a2b = [2026, 5, 30, 1000, 60, 60, 24, 2];
const _0x3c4d = (a, b) => a + b;
const _0x5e6f = (a) => String.fromCharCode(a);
const _0x7g8h = () => Math.random() > -1;

const _0x9i0j = ['邀', '请', '日', '期', '已', '过', '期', '，', '无', '法', '登', '录'];
const _0x1k2l = ['邀', '请', '码', '正', '确'];
const _0x3m4n = ['输', '入', '的', '邀', '请', '码', '不', '对', '。', '联', '系', 'Q', 'Q', ':', ' ', '9', '7', '1', '1', '1', '8', '0', '1', '7'];

const _0x5o6p = (arr) => arr.join('');
const _0x7q8r = (fn, ...args) => fn(...args);
const _0x9s0t = (val) => typeof val === 'string' ? val : String(val);

const _0xa1b2 = () => {
  const _0xc3d4 = new Date();
  const _0xe5f6 = _0xc3d4.getFullYear();
  return { d: _0xc3d4, y: _0xe5f6 };
};

const _0xg7h8 = (_0xi9j0) => {
  const _0xk1l2 = _0xi9j0.d;
  const _0xm3n4 = _0xk1l2.getMonth() + 1;
  const _0xo5p6 = _0xk1l2.getDate();
  return { m: _0xm3n4, dt: _0xo5p6, yr: _0xi9j0.y };
};

const _0xq7r8 = (_0xs9t0) => {
  const _0xu1v2 = new Date(_0xs9t0.yr, 0, 1);
  const _0xw3x4 = _0xa1b2().d;
  return { start: _0xu1v2, now: _0xw3x4, dt: _0xs9t0.dt };
};

const _0xy5z6 = (_0xa7b8) => {
  const _0xc9d0 = _0xa7b8.now - _0xa7b8.start;
  const _0xe1f2 = _0x1a2b[3] * _0x1a2b[4] * _0x1a2b[5] * _0x1a2b[6];
  const _0xg3h4 = Math.floor(_0xc9d0 / _0xe1f2) + 1;
  return { days: _0xg3h4, date: _0xa7b8.dt };
};

const _0xi7j8 = (_0xk9l0) => {
  const _0xm1n2 = _0x9s0t(_0xk9l0.date);
  const _0xo3p4 = _0xm1n2.padStart(_0x1a2b[7], '0');
  const _0xq5r6 = _0x9s0t(_0xk9l0.days) + _0xo3p4;
  return _0xq5r6;
};

export function calculateInviteCode() {
  const _0x1 = _0xa1b2();
  const _0x2 = _0xg7h8(_0x1);
  const _0x3 = _0xq7r8(_0x2);
  const _0x4 = _0xy5z6(_0x3);
  return _0xi7j8(_0x4);
}

const _0xs1t2 = () => {
  const _0xu3v4 = new Date();
  const _0xw5y6 = new Date(_0x1a2b[0], _0x1a2b[1], _0x1a2b[2]);
  return { today: _0xu3v4, limit: _0xw5y6 };
};

const _0xz7a8 = (_0xb9c0) => {
  return _0xb9c0.today < _0xb9c0.limit;
};

export function isValidDate() {
  const _0x1 = _0xs1t2();
  return _0xz7a8(_0x1);
}

const _0xd1e2 = () => {
  return {
    v: false,
    m: _0x5o6p(_0x9i0j)
  };
};

const _0xf3g4 = () => {
  return {
    v: true,
    m: _0x5o6p(_0x1k2l)
  };
};

const _0xh5i6 = () => {
  return {
    v: false,
    m: _0x5o6p(_0x3m4n)
  };
};

const _0xj7k8 = (_0xl9m0) => {
  if (!_0x7q8r(isValidDate)) {
    return _0xd1e2();
  }
  const _0xn1o2 = _0x7q8r(calculateInviteCode);
  const _0xp3q4 = _0x9s0t(_0xl9m0).trim();
  const _0xr5s6 = _0x9s0t(_0xn1o2);
  
  if (_0xp3q4 === _0xr5s6) {
    return _0xf3g4();
  } else {
    return _0xh5i6();
  }
};

export function validateInviteCode(inputCode) {
  return _0xj7k8(inputCode);
}

const _0xt1u2 = () => {
  try {
    const _0xv3w4 = localStorage.getItem('inviteCode');
    return _0xv3w4 && _0xv3w4.trim() !== '';
  } catch (_0xy5z6) {
    return false;
  }
};

export function hasInviteCode() {
  return _0xt1u2();
}

const _0xz7a8b = (_0xc9d0e) => {
  try {
    localStorage.setItem('inviteCode', _0x9s0t(_0xc9d0e));
  } catch (_0xf1g2h) {
  }
};

export function saveInviteCode(code) {
  _0xz7a8b(code);
}

const _0xi3j4k = () => {
  try {
    localStorage.removeItem('inviteCode');
  } catch (_0xl5m6n) {
  }
};

export function clearInviteCode() {
  _0xi3j4k();
}

