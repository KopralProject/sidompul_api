const TelegramBot = require('node-telegram-bot-api');
const { exec } = require('child_process');

// Ganti dengan token bot Telegram Anda
const TOKEN = '8187353779:AAGps6cekrxUmKvYnXV9janleVGRd3wYuE8';

// Inisialisasi bot dengan polling
const bot = new TelegramBot(TOKEN, { polling: true });

// Fungsi menjalankan script sidompul.sh dengan nomor XL
function cekPaketXL(nomor) {
  return new Promise((resolve, reject) => {
    exec(`./sidompul.sh ${nomor}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error menjalankan script: ${stderr || error.message}`);
      } else {
        resolve(stdout);
      }
    });
  });
}

// Tangani pesan masuk
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text.trim();

  // Validasi input nomor XL (minimal 10 digit angka)
  if (!/^\d{10,}$/.test(text)) {
    bot.sendMessage(chatId, 'Mohon kirim nomor XL yang valid (minimal 10 digit angka).');
    return;
  }

  bot.sendMessage(chatId, 'Sedang memproses, mohon tunggu...');

  try {
    const hasil = await cekPaketXL(text);
    bot.sendMessage(chatId, `Hasil cek paket XL:\n\n${hasil}`);
  } catch (err) {
    bot.sendMessage(chatId, `Terjadi kesalahan:\n${err}`);
  }
});

console.log('Bot Telegram Paket XL berjalan...');
