import streamlit as st
import music21
from music21 import stream, note, chord, meter, key, tempo
import io
import base64

st.set_page_config(page_title="Track to Track AI", layout="wide")

st.title("🎵 Track to Track AI")
st.markdown("Gere trilhas MIDI instantaneamente!")

# Interface
col1, col2 = st.columns([1,2])

with col1:
    st.header("🎛️ Parâmetros")
    genres = ["Pop", "Rock", "EDM", "Gospel", "Bossa Nova", "Jazz", "Funk"]
    genre = st.selectbox("Estilo", genres)
    bpm = st.slider("BPM", 60, 180, 120)
    section = st.selectbox("Seção", ["Intro", "Verso", "Refrão"])
    
if st.button("🎨 **GERAR MIDI**", type="primary", use_container_width=True):
    with st.spinner("🎼 Criando sua trilha..."):
        # Criar partitura music21
        score = stream.Score()
        part = stream.Part()
        
        # Configurações básicas
        ts = meter.TimeSignature('4/4')
        part.append(ts)
        part.append(tempo.MetronomeMark(number=bpm))
        
        # Progressões por gênero
        progressions = {
            "Pop": [["C4","E4","G4"], ["F4","A4","C5"], ["G4","B4","D5"], ["C4","E4","G4"]],
            "Gospel": [["C4","E4","G4"], ["F4","A4","C5"], ["G4","B4","D5"], ["Am4","C5","E5"]],
            "Rock": [["E4","G#4","B4"], ["A4","C#5","E5"], ["D5","F#5","A5"], ["E4","G#4","B4"]],
            "EDM": [["C4","G4","C5"], ["A3","E4","A4"], ["F4","C5","F5"], ["G4","D5","G5"]],
            "Bossa Nova": [["Am7","Dm7","G7","Cmaj7"]]
        }
        
        prog = progressions.get(genre, [["C4","E4","G4"]])
        
        for i in range(8):  # 8 compassos
            m = stream.Measure()
            chord_notes = prog[i % len(prog)]
            ch = chord.Chord(chord_notes)
            ch.duration.quarterLength = 4
            m.append(ch)
            part.append(m)
        
        score.append(part)
        
        # Download MIDI
        buffer = io.BytesIO()
        score.write('midi', fp=buffer)
        b64 = base64.b64encode(buffer.getvalue()).decode()
        filename = f"{genre}_{section}.mid"
        href = f'<a href="data:audio/midi;base64,{b64}" download="{filename}">📥 Baixar {filename}</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        st.balloons()
        st.success(f"✅ {genre} {section} gerada! Abra no seu DAW 🎹")

# Sidebar
with st.sidebar:
    st.header("📋 Como usar")
    st.markdown("""
    1. Escolha estilo musical
    2. Ajuste BPM
    3. Selecione seção
    4. Clique gerar
    5. Baixe .mid e abra no FL Studio/Ableton
    """)
    
st.markdown("---")
st.markdown("*Track to Track AI v1.0* | Feito com ❤️ para produtores BR 🇧🇷")
