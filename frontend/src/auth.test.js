import { getToken, setToken, clearToken, authHeaders } from './auth';

// Mock localStorage
const mockLocalStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

// Replace global localStorage with mock
Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

describe('Auth utilities', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getToken', () => {
    it('returns null when no token is stored', () => {
      mockLocalStorage.getItem.mockReturnValue(null);
      expect(getToken()).toBeNull();
    });

    it('returns the stored token', () => {
      const token = 'test-token-123';
      mockLocalStorage.getItem.mockReturnValue(token);
      expect(getToken()).toBe(token);
    });
  });

  describe('setToken', () => {
    it('stores the token in localStorage', () => {
      const token = 'test-token-456';
      setToken(token);
      expect(mockLocalStorage.setItem).toHaveBeenCalledWith('token', token);
    });
  });

  describe('clearToken', () => {
    it('removes the token from localStorage', () => {
      clearToken();
      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('token');
    });
  });

  describe('authHeaders', () => {
    it('returns empty object when no token exists', () => {
      mockLocalStorage.getItem.mockReturnValue(null);
      expect(authHeaders()).toEqual({});
    });

    it('returns authorization header when token exists', () => {
      const token = 'test-token-789';
      mockLocalStorage.getItem.mockReturnValue(token);
      expect(authHeaders()).toEqual({ Authorization: `Bearer ${token}` });
    });
  });
});