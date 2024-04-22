# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 25/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import uuid

from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, Float, TIMESTAMP, ARRAY, UniqueConstraint, \
    ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.connection import Base


# Base = declarative_base()

class Users(Base):
    __tablename__ = 'tbl_user'

    kode_user = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.uuid_generate_v4())
    username = Column(String(28), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    nama_depan = Column(String(25))
    nama_belakang = Column(String(25))
    alamat = Column(Text)
    level = Column(Enum('Admin', 'Pengguna', name='user_level'), nullable=False, default='Pengguna')
    status = Column(Enum('Active', 'Banned', name='user_status'), nullable=False)
    avatar = Column(String(255))
    created_at = Column(TIMESTAMP, server_default='now()')
    deleted_at = Column(TIMESTAMP)

    # Indexes
    __table_args__ = (
        UniqueConstraint('email', name='email_idx'),
        UniqueConstraint('username', name='username_pk')
    )

class PasswordHash(Base):
    __tablename__ = 'tbl_password_hash'

    kode_user = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    salt = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False, unique=True)

class DetailPengguna(Base):
    __tablename__ = 'tbl_detail_pengguna'

    kode_peternakan = Column(Integer, primary_key=True)
    kode_user = Column(UUID(as_uuid=True), ForeignKey('tbl_user.kode_user'), nullable=False)
    nama_peternakan = Column(String, nullable=False)
    alamat_peternakan = Column(Text, nullable=False)

    user = relationship('Users', back_populates='detail_pengguna')
    riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='peternakan')

class BasePenyakit(Base):
    __tablename__ = 'tbl_penyakit'

    kode_penyakit = Column(String(3), primary_key=True)
    nama_penyakit = Column(String(40), nullable=False)
    definisi = Column(Text)
    penyebab = Column(Text)
    penularan = Column(Text)
    pencegahan = Column(Text)
    penanganan = Column(Text)
    gambar = Column(String)
    created_at = Column(TIMESTAMP, default=func.now(), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    rule = relationship('Rule', back_populates='penyakit')
    riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='penyakit')

class BaseGejala(Base):
    __tablename__ = 'tbl_gejala'

    kode_gejala = Column(String(3), primary_key=True)
    gejala = Column(Text)

    rule = relationship('Rule', back_populates='gejala')
    # riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='riwayat_diagnosa')

class Rule(Base):
    __tablename__ = 'tbl_rule'

    kode_penyakit = Column(String, ForeignKey('tbl_penyakit.kode_penyakit'), primary_key=True)
    kode_gejala = Column(String, ForeignKey('tbl_gejala.kode_gejala'), primary_key=True)
    belief = Column(Float)

    # Relationships
    penyakit = relationship('BasePenyakit', back_populates='rule')
    gejala = relationship('BaseGejala', back_populates='rule')

class RiwayatDiagnosa(Base):
    __tablename__ = 'tbl_riwayat_diagnosa'

    kode_riwayat = Column(Integer, primary_key=True)
    kode_pengguna = Column(UUID(as_uuid=True), ForeignKey('tbl_user.kode_user'))
    kode_peternakan = Column(Integer, ForeignKey('tbl_detail_pengguna.kode_peternakan'))
    kode_penyakit = Column(String(3), ForeignKey('tbl_penyakit.kode_penyakit'))
    kode_gejala = Column(ARRAY(String))
    prosentase = Column(Float)
    kesimpulan = Column(Text)

    # Relationshipsalembic stamp head
    user = relationship('Users', back_populates='riwayat_diagnosa')
    peternakan = relationship('DetailPengguna', back_populates='riwayat_diagnosa')
    penyakit = relationship('BasePenyakit', back_populates='riwayat_diagnosa')
    # gejala = relationship('BaseGejala', back_populates='riwayat_diagnosa')

# Additional relationships or constraints can be added as needed
Users.detail_pengguna = relationship('DetailPengguna', back_populates='user')
Users.riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='user')
DetailPengguna.user = relationship('Users', back_populates='detail_pengguna')
DetailPengguna.riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='peternakan')
BasePenyakit.rule = relationship('Rule', back_populates='penyakit')
BasePenyakit.riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='penyakit')
BaseGejala.rule = relationship('Rule', back_populates='gejala')
# BaseGejala.riwayat_diagnosa = relationship('RiwayatDiagnosa', back_populates='gejala')
