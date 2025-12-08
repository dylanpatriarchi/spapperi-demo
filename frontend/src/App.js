import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  background: white;
  padding: 20px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
`;

const Header = styled.header`
  text-align: center;
  color: #333;
  margin-bottom: 40px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin: 0 0 10px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
`;

const Subtitle = styled.p`
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
`;

const ChatContainer = styled.div`
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 80vh;
`;

const StatsBar = styled.div`
  background: #f8f9fa;
  padding: 15px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const StatItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #666;
`;

const StatusDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.active ? '#4caf50' : '#f44336'};
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #fafafa;
`;

const Message = styled.div`
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: ${props => props.isUser ? 'flex-end' : 'flex-start'};
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 12px 18px;
  border-radius: 18px;
  background: ${props => props.isUser ? '#667eea' : '#ffffff'};
  color: ${props => props.isUser ? 'white' : '#333'};
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
  
  p {
    margin: 0.5em 0;
  }
  
  p:first-child {
    margin-top: 0;
  }
  
  p:last-child {
    margin-bottom: 0;
  }
`;

const MessageLabel = styled.div`
  font-size: 0.75rem;
  color: #999;
  margin-bottom: 5px;
  padding: 0 10px;
`;

const Sources = styled.div`
  margin-top: 10px;
  padding: 10px;
  background: #f0f0f0;
  border-radius: 8px;
  font-size: 0.85rem;
`;

const SourceItem = styled.div`
  margin: 5px 0;
  color: #666;
`;

const InputContainer = styled.div`
  padding: 20px;
  background: white;
  border-top: 1px solid #e0e0e0;
`;

const InputForm = styled.form`
  display: flex;
  gap: 10px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
  
  &:focus {
    border-color: #333;
  }
`;

const Button = styled.button`
  padding: 12px 30px;
  background: #333;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const LoadingDots = styled.div`
  display: flex;
  gap: 5px;
  padding: 15px;
  
  span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
    animation: bounce 1.4s infinite ease-in-out both;
    
    &:nth-child(1) {
      animation-delay: -0.32s;
    }
    
    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
  
  @keyframes bounce {
    0%, 80%, 100% {
      transform: scale(0);
    }
    40% {
      transform: scale(1);
    }
  }
`;



function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [health, setHealth] = useState(null);
  const messagesEndRef = useRef(null);



  useEffect(() => {
    fetchHealth();
    fetchStats();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchHealth = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`);
      setHealth(response.data);
    } catch (error) {
      console.error('Error fetching health:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleSubmit = async (e, question = null) => {
    e?.preventDefault();
    const questionText = question || input;

    if (!questionText.trim()) return;

    const userMessage = {
      type: 'user',
      content: questionText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/query`, {
        question: questionText
      });

      const assistantMessage = {
        type: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        type: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };



  return (
    <AppContainer>
      <Header>
        <Title>🌾 Spapperi RAG Agent</Title>
        <Subtitle>AI-Powered Assistant for Agricultural Machinery</Subtitle>
      </Header>

      <ChatContainer>
        <StatsBar>
          <StatItem>
            <StatusDot active={health?.database_connected} />
            <span>{health?.database_connected ? 'Connected' : 'Disconnected'}</span>
          </StatItem>
          <StatItem>
            📚 {stats?.total_documents || 0} documents loaded
          </StatItem>
          <StatItem>
            📁 {stats?.unique_sources || 0} sources
          </StatItem>
        </StatsBar>

        <MessagesContainer>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: '#999' }}>
              <h2>👋 Welcome!</h2>
              <p>Ask me anything about Spapperi's agricultural machinery and products.</p>
              <p style={{ fontSize: '0.9rem', marginTop: '20px', color: '#666' }}>
                Ask me anything about Spapperi's agricultural machinery and products.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <Message key={index} isUser={message.type === 'user'}>
              <MessageLabel>
                {message.type === 'user' ? 'You' : 'Spapperi Assistant'}
              </MessageLabel>
              <MessageBubble isUser={message.type === 'user'}>
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </MessageBubble>
              {message.sources && message.sources.length > 0 && (
                <Sources>
                  <strong>Sources:</strong>
                  {message.sources.map((source, idx) => (
                    <SourceItem key={idx}>
                      📄 {source.source} (relevance: {(source.relevance_score * 100).toFixed(0)}%)
                    </SourceItem>
                  ))}
                </Sources>
              )}
            </Message>
          ))}

          {loading && (
            <Message isUser={false}>
              <MessageLabel>Spapperi Assistant</MessageLabel>
              <MessageBubble>
                <LoadingDots>
                  <span></span>
                  <span></span>
                  <span></span>
                </LoadingDots>
              </MessageBubble>
            </Message>
          )}

          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputContainer>
          <InputForm onSubmit={handleSubmit}>
            <Input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about Spapperi products..."
              disabled={loading}
            />
            <Button type="submit" disabled={loading || !input.trim()}>
              {loading ? 'Sending...' : 'Send'}
            </Button>
          </InputForm>
        </InputContainer>
      </ChatContainer>
    </AppContainer>
  );
}

export default App;


