{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyObn7bjNo4WnqKAP4LpZwwV",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/hyewon7011/jju/blob/main/250102_06_01_PDFLoader.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#PDFLoader\n",
        "\n"
      ],
      "metadata": {
        "id": "tGKamXuyxK-H"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "id": "CjySCGrKu6Kz"
      },
      "outputs": [],
      "source": [
        "FILE_PATH = \"/content/SPRI_AI_Brief_2023년12월호_F.pdf\""
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def show_metadata(docs):\n",
        "    if docs:\n",
        "        print(\"[metadata]\")\n",
        "        print(list(docs[0].metadata.keys()))\n",
        "        print(\"\\n[examples]\")\n",
        "        max_key_length = max(len(k) for k in docs[0].metadata.keys())\n",
        "        for k, v in docs[0].metadata.items():\n",
        "            print(f\"{k:<{max_key_length}} : {v}\")"
      ],
      "metadata": {
        "id": "gQPH3otQxWxW"
      },
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#PyPDF\n",
        "여기에서는 pypdf를 사용하여 PDF를 문서 배열로 로드하며, 각 문서는 page 번호와 함께 페이지 내용 및 메타데이터를 포함합니다."
      ],
      "metadata": {
        "id": "ueKnuX4wxYyi"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -qU pypdf"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "1jMsdtc8xdEP",
        "outputId": "d03d5ac6-9b4b-45f5-c0ee-fa7f7f1c9023"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/298.0 kB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━\u001b[0m\u001b[91m╸\u001b[0m\u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m71.7/298.0 kB\u001b[0m \u001b[31m2.2 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[91m╸\u001b[0m \u001b[32m297.0/298.0 kB\u001b[0m \u001b[31m4.4 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m298.0/298.0 kB\u001b[0m \u001b[31m3.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -qU langchain_community"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "nKqx2_2ByArg",
        "outputId": "06d84e54-ff6c-498c-a0fb-44e6bc3e9819"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/2.5 MB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[91m━━━━━\u001b[0m\u001b[90m╺\u001b[0m\u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.3/2.5 MB\u001b[0m \u001b[31m9.7 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[90m╺\u001b[0m\u001b[90m━━━━━━━━━━━━━\u001b[0m \u001b[32m1.6/2.5 MB\u001b[0m \u001b[31m23.3 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m2.5/2.5 MB\u001b[0m \u001b[31m24.6 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/1.0 MB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.0/1.0 MB\u001b[0m \u001b[31m46.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m411.6/411.6 kB\u001b[0m \u001b[31m27.1 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m49.3/49.3 kB\u001b[0m \u001b[31m4.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from langchain_community.document_loaders import PyPDFLoader\n",
        "\n",
        "# 파일 경로 설정\n",
        "loader = PyPDFLoader(FILE_PATH)\n",
        "\n",
        "# PDF 로더 초기화\n",
        "docs = loader.load()\n",
        "\n",
        "# 문서의 내용 출력\n",
        "print(docs[10].page_content[:300])\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "G8FAMlbJx0vX",
        "outputId": "5d926943-c7ab-4288-e10c-716c92cfad25"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "SPRi AI Brief |  2023-12월호\n",
            "8\n",
            "코히어, 데이터 투명성 확보를 위한 데이터 출처 탐색기 공개n코히어와 12개 기관이  광범위한 데이터셋에 대한 감사를 통해 원본 데이터 출처, 재라이선스 상태, 작성자 등 다양한 정보를 제공하는 ‘데이터 출처 탐색기’ 플랫폼을 출시n대화형 플랫폼을 통해 개발자는 데이터셋의 라이선스 상태를 쉽게 파악할 수 있으며 데이터셋의 구성과 계보도 추적 가능\n",
            "KEY Contents\n",
            "£데이터 출처 탐색기, 광범위한 데이터셋 정보 제공을 통해 데이터 투명성 향상nAI 기업 코히어(Cohere)가 \n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 문서의 내용 출력\n",
        "print(docs[20].page_content[:300])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4slwFUcSyNmY",
        "outputId": "6ffcc61e-cc6a-46bb-d44e-3e536d75991b"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "18\n",
            "영국 옥스퍼드 인터넷 연구소, AI 기술자의 임금이 평균 21% 높아n옥스퍼드 인터넷 연구소의 연구에 따르면 특정 기술의 경제적 가치는 다른 기술과 결합 가능성이 높을수록 높게 평가됨 nAI의 확산은 기술의 경제적 가치에 크게 영향을 미치며, AI 기술을 가진 근로자는 평균 21%, 최대 40% 높은 임금을 받을 수 있음  \n",
            "KEY Contents\n",
            "£AI 기술 중 머신러닝, 텐서플로우, 딥러닝의 임금 프리미엄이 높게 평가n옥스퍼드 인터넷 연구소(Oxford Internet Institute)가 2023년 10월 24일 962개\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#PyMuPDF\n",
        "PyMuPDF 는 속도 최적화가 되어 있으며, PDF 및 해당 페이지에 대한 자세한 메타데이터를 포함하고 있습니다. 페이지 당 하나의 문서를 반환합니다:"
      ],
      "metadata": {
        "id": "HYEx1h81zk5o"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -qU pymupdf"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2dKH--nvzpkX",
        "outputId": "821be6ba-6e9a-422a-f069-4a0d1530e743"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m20.0/20.0 MB\u001b[0m \u001b[31m59.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from langchain_community.document_loaders import PyMuPDFLoader\n",
        "\n",
        "# PyMuPDF 로더 인스턴스 생성\n",
        "loader = PyMuPDFLoader(FILE_PATH)\n",
        "\n",
        "# 문서 로드\n",
        "docs = loader.load()"
      ],
      "metadata": {
        "id": "fXYP3f9-yNg1"
      },
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# 문서의 내용 출력\n",
        "print(docs[10].page_content[:300])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "WFPhC6wpzxwP",
        "outputId": "3ec38751-4499-48da-dc26-d8b16fef9341"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "SPRi AI Brief |  \n",
            "2023-12월호\n",
            "8\n",
            "코히어, 데이터 투명성 확보를 위한 데이터 출처 탐색기 공개\n",
            "n 코히어와 12개 기관이  광범위한 데이터셋에 대한 감사를 통해 원본 데이터 출처, 재라이선스 상태, \n",
            "작성자 등 다양한 정보를 제공하는 ‘데이터 출처 탐색기’ 플랫폼을 출시\n",
            "n 대화형 플랫폼을 통해 개발자는 데이터셋의 라이선스 상태를 쉽게 파악할 수 있으며 데이터셋의 \n",
            "구성과 계보도 추적 가능\n",
            "KEY Contents\n",
            "£ 데이터 출처 탐색기, 광범위한 데이터셋 정보 제공을 통해 데이터 투명성 향상\n",
            "n AI 기업 코히어\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [],
      "metadata": {
        "id": "M-wzqg-51QiE"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -qU pypdfium2"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GYWtCQF11QTK",
        "outputId": "4aa4f403-de48-44e7-8af2-8f768d85030b"
      },
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[?25l     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/48.2 kB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m48.2/48.2 kB\u001b[0m \u001b[31m1.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/2.9 MB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[91m━━━━\u001b[0m\u001b[90m╺\u001b[0m\u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.3/2.9 MB\u001b[0m \u001b[31m8.4 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[90m╺\u001b[0m\u001b[90m━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.7/2.9 MB\u001b[0m \u001b[31m24.0 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m2.9/2.9 MB\u001b[0m \u001b[31m28.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from langchain_community.document_loaders import PyPDFium2Loader\n",
        "\n",
        "# PyPDFium2 로더 인스턴스 생성\n",
        "loader = PyPDFium2Loader(FILE_PATH)\n",
        "\n",
        "# 데이터 로드\n",
        "docs = loader.load()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "jzFB1r281IxW",
        "outputId": "0e52a236-bca0-4492-c0bb-b5edeee4c073"
      },
      "execution_count": 20,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "/usr/local/lib/python3.10/dist-packages/pypdfium2/_helpers/textpage.py:80: UserWarning: get_text_range() call with default params will be implicitly redirected to get_text_bounded()\n",
            "  warnings.warn(\"get_text_range() call with default params will be implicitly redirected to get_text_bounded()\")\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#PDFMiner"
      ],
      "metadata": {
        "id": "isMARnYirXdl"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -qU pdfminer.six"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JF7rLRarrgv6",
        "outputId": "74758506-2496-44b1-c71f-c19a501b0e7d"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/5.6 MB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━\u001b[0m\u001b[91m╸\u001b[0m\u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m2.2/5.6 MB\u001b[0m \u001b[31m65.5 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[91m╸\u001b[0m \u001b[32m5.6/5.6 MB\u001b[0m \u001b[31m103.4 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m5.6/5.6 MB\u001b[0m \u001b[31m64.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install langchain_community"
      ],
      "metadata": {
        "collapsed": true,
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "eGfY1V5vsp4J",
        "outputId": "96a7541d-d0e8-4980-c1e0-ee188a829753"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting langchain_community\n",
            "  Downloading langchain_community-0.3.13-py3-none-any.whl.metadata (2.9 kB)\n",
            "Requirement already satisfied: PyYAML>=5.3 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (6.0.2)\n",
            "Requirement already satisfied: SQLAlchemy<3,>=1.4 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (2.0.36)\n",
            "Requirement already satisfied: aiohttp<4.0.0,>=3.8.3 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (3.11.10)\n",
            "Collecting dataclasses-json<0.7,>=0.5.7 (from langchain_community)\n",
            "  Downloading dataclasses_json-0.6.7-py3-none-any.whl.metadata (25 kB)\n",
            "Collecting httpx-sse<0.5.0,>=0.4.0 (from langchain_community)\n",
            "  Downloading httpx_sse-0.4.0-py3-none-any.whl.metadata (9.0 kB)\n",
            "Collecting langchain<0.4.0,>=0.3.13 (from langchain_community)\n",
            "  Downloading langchain-0.3.13-py3-none-any.whl.metadata (7.1 kB)\n",
            "Collecting langchain-core<0.4.0,>=0.3.27 (from langchain_community)\n",
            "  Downloading langchain_core-0.3.28-py3-none-any.whl.metadata (6.3 kB)\n",
            "Requirement already satisfied: langsmith<0.3,>=0.1.125 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (0.2.3)\n",
            "Requirement already satisfied: numpy<2,>=1.22.4 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (1.26.4)\n",
            "Collecting pydantic-settings<3.0.0,>=2.4.0 (from langchain_community)\n",
            "  Downloading pydantic_settings-2.7.1-py3-none-any.whl.metadata (3.5 kB)\n",
            "Requirement already satisfied: requests<3,>=2 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (2.32.3)\n",
            "Requirement already satisfied: tenacity!=8.4.0,<10,>=8.1.0 in /usr/local/lib/python3.10/dist-packages (from langchain_community) (9.0.0)\n",
            "Requirement already satisfied: aiohappyeyeballs>=2.3.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (2.4.4)\n",
            "Requirement already satisfied: aiosignal>=1.1.2 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (1.3.2)\n",
            "Requirement already satisfied: async-timeout<6.0,>=4.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (4.0.3)\n",
            "Requirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (24.3.0)\n",
            "Requirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (1.5.0)\n",
            "Requirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (6.1.0)\n",
            "Requirement already satisfied: propcache>=0.2.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (0.2.1)\n",
            "Requirement already satisfied: yarl<2.0,>=1.17.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain_community) (1.18.3)\n",
            "Collecting marshmallow<4.0.0,>=3.18.0 (from dataclasses-json<0.7,>=0.5.7->langchain_community)\n",
            "  Downloading marshmallow-3.23.2-py3-none-any.whl.metadata (7.1 kB)\n",
            "Collecting typing-inspect<1,>=0.4.0 (from dataclasses-json<0.7,>=0.5.7->langchain_community)\n",
            "  Downloading typing_inspect-0.9.0-py3-none-any.whl.metadata (1.5 kB)\n",
            "Requirement already satisfied: langchain-text-splitters<0.4.0,>=0.3.3 in /usr/local/lib/python3.10/dist-packages (from langchain<0.4.0,>=0.3.13->langchain_community) (0.3.3)\n",
            "Requirement already satisfied: pydantic<3.0.0,>=2.7.4 in /usr/local/lib/python3.10/dist-packages (from langchain<0.4.0,>=0.3.13->langchain_community) (2.10.3)\n",
            "Requirement already satisfied: jsonpatch<2.0,>=1.33 in /usr/local/lib/python3.10/dist-packages (from langchain-core<0.4.0,>=0.3.27->langchain_community) (1.33)\n",
            "Requirement already satisfied: packaging<25,>=23.2 in /usr/local/lib/python3.10/dist-packages (from langchain-core<0.4.0,>=0.3.27->langchain_community) (24.2)\n",
            "Requirement already satisfied: typing-extensions>=4.7 in /usr/local/lib/python3.10/dist-packages (from langchain-core<0.4.0,>=0.3.27->langchain_community) (4.12.2)\n",
            "Requirement already satisfied: httpx<1,>=0.23.0 in /usr/local/lib/python3.10/dist-packages (from langsmith<0.3,>=0.1.125->langchain_community) (0.28.1)\n",
            "Requirement already satisfied: orjson<4.0.0,>=3.9.14 in /usr/local/lib/python3.10/dist-packages (from langsmith<0.3,>=0.1.125->langchain_community) (3.10.12)\n",
            "Requirement already satisfied: requests-toolbelt<2.0.0,>=1.0.0 in /usr/local/lib/python3.10/dist-packages (from langsmith<0.3,>=0.1.125->langchain_community) (1.0.0)\n",
            "Collecting python-dotenv>=0.21.0 (from pydantic-settings<3.0.0,>=2.4.0->langchain_community)\n",
            "  Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2->langchain_community) (3.4.0)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2->langchain_community) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2->langchain_community) (2.2.3)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2->langchain_community) (2024.12.14)\n",
            "Requirement already satisfied: greenlet!=0.4.17 in /usr/local/lib/python3.10/dist-packages (from SQLAlchemy<3,>=1.4->langchain_community) (3.1.1)\n",
            "Requirement already satisfied: anyio in /usr/local/lib/python3.10/dist-packages (from httpx<1,>=0.23.0->langsmith<0.3,>=0.1.125->langchain_community) (3.7.1)\n",
            "Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.10/dist-packages (from httpx<1,>=0.23.0->langsmith<0.3,>=0.1.125->langchain_community) (1.0.7)\n",
            "Requirement already satisfied: h11<0.15,>=0.13 in /usr/local/lib/python3.10/dist-packages (from httpcore==1.*->httpx<1,>=0.23.0->langsmith<0.3,>=0.1.125->langchain_community) (0.14.0)\n",
            "Requirement already satisfied: jsonpointer>=1.9 in /usr/local/lib/python3.10/dist-packages (from jsonpatch<2.0,>=1.33->langchain-core<0.4.0,>=0.3.27->langchain_community) (3.0.0)\n",
            "Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.10/dist-packages (from pydantic<3.0.0,>=2.7.4->langchain<0.4.0,>=0.3.13->langchain_community) (0.7.0)\n",
            "Requirement already satisfied: pydantic-core==2.27.1 in /usr/local/lib/python3.10/dist-packages (from pydantic<3.0.0,>=2.7.4->langchain<0.4.0,>=0.3.13->langchain_community) (2.27.1)\n",
            "Collecting mypy-extensions>=0.3.0 (from typing-inspect<1,>=0.4.0->dataclasses-json<0.7,>=0.5.7->langchain_community)\n",
            "  Downloading mypy_extensions-1.0.0-py3-none-any.whl.metadata (1.1 kB)\n",
            "Requirement already satisfied: sniffio>=1.1 in /usr/local/lib/python3.10/dist-packages (from anyio->httpx<1,>=0.23.0->langsmith<0.3,>=0.1.125->langchain_community) (1.3.1)\n",
            "Requirement already satisfied: exceptiongroup in /usr/local/lib/python3.10/dist-packages (from anyio->httpx<1,>=0.23.0->langsmith<0.3,>=0.1.125->langchain_community) (1.2.2)\n",
            "Downloading langchain_community-0.3.13-py3-none-any.whl (2.5 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m2.5/2.5 MB\u001b[0m \u001b[31m51.5 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading dataclasses_json-0.6.7-py3-none-any.whl (28 kB)\n",
            "Downloading httpx_sse-0.4.0-py3-none-any.whl (7.8 kB)\n",
            "Downloading langchain-0.3.13-py3-none-any.whl (1.0 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.0/1.0 MB\u001b[0m \u001b[31m43.5 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading langchain_core-0.3.28-py3-none-any.whl (411 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m411.6/411.6 kB\u001b[0m \u001b[31m25.2 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading pydantic_settings-2.7.1-py3-none-any.whl (29 kB)\n",
            "Downloading marshmallow-3.23.2-py3-none-any.whl (49 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m49.3/49.3 kB\u001b[0m \u001b[31m3.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)\n",
            "Downloading typing_inspect-0.9.0-py3-none-any.whl (8.8 kB)\n",
            "Downloading mypy_extensions-1.0.0-py3-none-any.whl (4.7 kB)\n",
            "Installing collected packages: python-dotenv, mypy-extensions, marshmallow, httpx-sse, typing-inspect, pydantic-settings, dataclasses-json, langchain-core, langchain, langchain_community\n",
            "  Attempting uninstall: langchain-core\n",
            "    Found existing installation: langchain-core 0.3.25\n",
            "    Uninstalling langchain-core-0.3.25:\n",
            "      Successfully uninstalled langchain-core-0.3.25\n",
            "  Attempting uninstall: langchain\n",
            "    Found existing installation: langchain 0.3.12\n",
            "    Uninstalling langchain-0.3.12:\n",
            "      Successfully uninstalled langchain-0.3.12\n",
            "Successfully installed dataclasses-json-0.6.7 httpx-sse-0.4.0 langchain-0.3.13 langchain-core-0.3.28 langchain_community-0.3.13 marshmallow-3.23.2 mypy-extensions-1.0.0 pydantic-settings-2.7.1 python-dotenv-1.0.1 typing-inspect-0.9.0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from langchain_community.document_loaders import PDFMinerLoader\n",
        "\n",
        "# PDFMiner 로더 인스턴스 생성\n",
        "loader = PDFMinerLoader(FILE_PATH)\n",
        "\n",
        "# 데이터 로드\n",
        "docs = loader.load()\n",
        "\n",
        "# 문서의 내용 출력\n",
        "print(docs[0].page_content[:300])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3rW3kYBRrXLz",
        "outputId": "6629d724-07af-4e01-f6f0-8f3cb7413ed3"
      },
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "2023년  12월호\n",
            "\n",
            "\f2023년  12월호\n",
            "\n",
            "Ⅰ.  인공지능  산업  동향  브리프\n",
            "\n",
            "  1.  정책/법제 \n",
            "\n",
            "      ▹  미국,  안전하고  신뢰할  수  있는  AI  개발과  사용에  관한  행정명령  발표    ························· 1\n",
            "\n",
            "      ▹  G7,  히로시마  AI  프로세스를  통해  AI  기업  대상  국제  행동강령에  합의 ··························· 2\n",
            "\n",
            "      ▹  영국  AI  안전성  정상회의에  참가한  28개국,  AI  위험에  공동 \n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader\n",
        "\n",
        "# PDFMinerPDFasHTMLLoader 인스턴스 생성\n",
        "loader = PDFMinerPDFasHTMLLoader(FILE_PATH)\n",
        "\n",
        "# 문서 로드\n",
        "docs = loader.load()\n",
        "\n",
        "# 문서의 내용 출력\n",
        "print(docs[0].page_content[:300])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bmQGVwDls-V6",
        "outputId": "067449a5-6be5-4297-c1e1-7e38cb9fbb69"
      },
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "<html><head>\n",
            "<meta http-equiv=\"Content-Type\" content=\"text/html\">\n",
            "</head><body>\n",
            "<span style=\"position:absolute; border: gray 1px solid; left:0px; top:50px; width:612px; height:858px;\"></span>\n",
            "<div style=\"position:absolute; top:50px;\"><a name=\"1\">Page 1</a></div>\n",
            "<div style=\"position:absolute; border\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 문서의 내용 출력\n",
        "print(docs[0].page_content[:1000])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "yg0iLPU1ti4Z",
        "outputId": "b9ae6990-a9bc-48e7-ed41-d780b7ac93b3"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "<html><head>\n",
            "<meta http-equiv=\"Content-Type\" content=\"text/html\">\n",
            "</head><body>\n",
            "<span style=\"position:absolute; border: gray 1px solid; left:0px; top:50px; width:612px; height:858px;\"></span>\n",
            "<div style=\"position:absolute; top:50px;\"><a name=\"1\">Page 1</a></div>\n",
            "<div style=\"position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:256px; top:332px; width:98px; height:20px;\"><span style=\"font-family: KoPubDotumBold; font-size:14px\">2023년  </span><span style=\"font-family: KoPubDotumBold; font-size:20px\">12</span><span style=\"font-family: KoPubDotumBold; font-size:14px\">월호\n",
            "<br></span></div><div style=\"position:absolute; border: figure 1px solid; writing-mode:False; left:0px; top:50px; width:612px; height:858px;\"></div><span style=\"position:absolute; border: gray 1px solid; left:0px; top:958px; width:612px; height:858px;\"></span>\n",
            "<div style=\"position:absolute; top:958px;\"><a name=\"2\">Page 2</a></div>\n",
            "<div style=\"position:absolute; border: textbox 1px solid; writing-mode:lr-tb;\n"
          ]
        }
      ]
    }
  ]
}