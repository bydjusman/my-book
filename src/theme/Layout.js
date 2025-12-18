import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import BookChatbot from '../components/BookChatbot';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
        <BookChatbot />
      </OriginalLayout>
    </>
  );
}