$target = Join-Path (Get-Location) 'frontend/public/audio/book-1'
New-Item -ItemType Directory -Force -Path $target | Out-Null
Add-Type -AssemblyName System.Speech
$items = @(
  @{ File = 'chapter-1.wav'; Text = 'The time traveller entered the room and looked carefully at the strange machine.' },
  @{ File = 'chapter-2.wav'; Text = 'The machine waited in silence while the wheels began to turn and the journey started.' },
  @{ File = 'chapter-3.wav'; Text = 'The journey continued through the ages, carrying a curious listener toward a new story.' }
)
foreach ($item in $items) {
  $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $speaker.Rate = 0
  $speaker.Volume = 100
  $speaker.SetOutputToWaveFile((Join-Path $target $item.File))
  $speaker.Speak($item.Text)
  $speaker.Dispose()
}
