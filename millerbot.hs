-- MillerBot
-- Haskell IRC Bot for no particular reason..
--
-- Author: Russell Miller
-- Start date: Jan 2011
-- GNU General Public License
-- http://www.gnu.org/licenses/gpl.html
--

import Network
import System.IO
import System.Exit
import Text.Printf
import Data.List
import Control.Arrow
import Control.Monad.Reader
import Control.Exception
import Prelude hiding (catch)


server = "irc.kittenz.pdx.edu"
port   = 6667
chan   = "#test"
nick   = "millerbot"


-- monad transformer to layer the Bot data type
type Net = ReaderT Bot IO

-- wrapper data type to work with socket
data Bot = Bot { socket :: Handle }


-- main function:
-- bracket takes 3 arguments: 
-- 1)a function to connect to the server 
-- 2)a function to disconnect
-- 3)main loop to run in between
main :: IO ()
main = bracket connect disconnect loop
 where
  disconnect = hClose . socket
  loop st    = runReaderT run st
  

-- connect function:
-- Connect to the server and return the initial bot state
connect :: IO Bot
connect = notify $ do
  h <- connectTo server (PortNumber (fromIntegral port))
  hSetBuffering h NoBuffering
  return (Bot h)
 where
  notify a = bracket_
             (printf "Connecting to %s ... " server >> hFlush stdout)
             (putStrLn "done.")
             a


-- run function:
-- Now in the Net monad, meaning connected.
-- Join a channel, start processing commands.
run :: Net ()
run = do
  write "NICK" nick
  write "USER" (nick ++ " 0 * :a useless bot")
  write "JOIN" chan
  asks socket >>= listen


-- listen function:
-- 1)pongs when ping is received, so as to stay connected
-- 2)clean removes leading ':' and everything up to the next ':'
-- 3)eval handles bot commands
listen :: Handle -> Net ()
listen h = forever $ do
  s <- init `fmap` io (hGetLine h)
  io (putStrLn s)
  if ping s then pong s else eval (clean s)
 where
  forever a = a >> forever a  
  clean     = drop 1 . dropWhile (/= ':') . drop 1
  ping x    = "PING :" `isPrefixOf` x
  pong x    = write "PONG" (':' : drop 6 x)


-- eval function:
-- Handle commands.
eval :: String -> Net ()
eval     "!quit"                = write "QUIT" ":Exiting" >> io (exitWith ExitSuccess)
eval x | "!echo" `isPrefixOf` x = privmsg (drop 6 x)
eval _                          = return ()  -- ignore everything else


-- privmsg function:
-- wrapper for write, sends message to channel
privmsg :: String -> Net ()
privmsg s = write "PRIVMSG" (chan ++ " :" ++ s)


-- write function:
-- Uses Net monad for sending data to server. Must be connected to do so.
-- Uses hPrintf to build an IRC message and write it to the server. 
-- For debugging purposes also prints the message to standard output.
write :: String -> String -> Net ()
write s t = do
  h <- asks socket
  io $ hPrintf h "%s %s\r\n" s t
  io $ printf    "> %s %s\n" s t


-- io function:
-- lift an IO expression into the Net monad 
-- making that IO function available to code in the Net monad
io :: IO a -> Net a
io = liftIO